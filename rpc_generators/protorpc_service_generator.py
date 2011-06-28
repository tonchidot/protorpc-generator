#/usr/env/bin python
from google.protobuf.descriptor import FieldDescriptor
from sys import stderr
import re

class ProtoRPCServiceGenerator(object):
	FIELD_TYPE_MAP = {
		FieldDescriptor.TYPE_DOUBLE:   'IntegerField',
		FieldDescriptor.TYPE_FLOAT:    'FloatField',
		FieldDescriptor.TYPE_INT64:    'IntegerField',
		FieldDescriptor.TYPE_UINT64:   'IntegerField',
		FieldDescriptor.TYPE_INT32:    'IntegerField',
		FieldDescriptor.TYPE_FIXED64:  'IntegerField',
		FieldDescriptor.TYPE_FIXED32:  'IntegerField',
		FieldDescriptor.TYPE_BOOL:     'BooleanField',
		FieldDescriptor.TYPE_STRING:   'StringField',
		FieldDescriptor.TYPE_MESSAGE:  'MessageField',
		FieldDescriptor.TYPE_BYTES:    'BytesField',
		FieldDescriptor.TYPE_UINT32:   'IntegerField',
		FieldDescriptor.TYPE_ENUM:     'EnumField',
		FieldDescriptor.TYPE_SFIXED32: 'IntegerField',
		FieldDescriptor.TYPE_SFIXED64: 'IntegerField',
		FieldDescriptor.TYPE_SINT32:   'IntegerField',
		FieldDescriptor.TYPE_SINT64:   'IntegerField',
	}
	def __init__(self):
		self.created_files = {}
	def genEnum(self, x, t=0):
		lines= \
			[ "%sclass %s(messages.Enum):"%("\t"*t, x.name) ] + \
			[ "%s%s = %i" % ("\t"*(t+1), e.name, e.number) for e in x.value] + \
			[ "" ]
		return lines
	def genExtension(self, x, t=0):
		raise NotImplementedError("Extensions not supported")
	def genExtensionRange(self, x, t=0):
		raise NotImplementedError("Extensions not supported")
	def genField(self, x, t=0):
		if x.extendee:
			raise NotImplementedError("Extendees not supported")
		if x.options.ctype:
			raise NotImplementedError("'ctype' not supported")
		if x.options.packed:
			raise NotImplementedError("'packed' not supported")
		kwargs=[]
		if x.label==FieldDescriptor.LABEL_REQUIRED: kwargs += ['required=True']
		if x.label==FieldDescriptor.LABEL_REPEATED: kwargs += ['repeated=True']
		if x.default_value:
			if ProtoRPCServiceGenerator.FIELD_TYPE_MAP[x.type]=='BooleanField':
				v=x.default_value.lower()
				if v=='true' or v=='1' or v=='yes':
					kwargs += ['default=True']
			elif ProtoRPCServiceGenerator.FIELD_TYPE_MAP[x.type]=='EnumField':
				kwargs += ["default='%s'"%x.default_value]
			elif ProtoRPCServiceGenerator.FIELD_TYPE_MAP[x.type]=='StringField':
				kwargs += ["default=%s"%repr(x.default_value)]
			else:
				kwargs += ['default=%s'%x.default_value]
		return ["%s%s = messages.%s(%s%i%s)%s"%(
			"\t"*t,
			x.name,
			ProtoRPCServiceGenerator.FIELD_TYPE_MAP[x.type],
			(x.type==FieldDescriptor.TYPE_MESSAGE or x.type==FieldDescriptor.TYPE_ENUM) \
				and "'%s',"%x.type_name[1:] \
				or '',
			x.number,
			len(kwargs) \
				and ', %s'%', '.join(kwargs) \
				or '',
			x.options.deprecated \
				and ' # deprecated!' \
				or ''
		)]
	def genMessage(self, x, t=0):
		# generate enums, messages, fields
		lines=[
			"%sclass %s(messages.Message):"%("\t"*t, x.name)
		]
		for xx in x.enum_type:
			lines+=self.genEnum(xx, t+1)
		for xx in x.extension:
			lines+=self.genExtension(xx, t+1)
		for xx in x.extension_range:
			lines+=self.genExtensionRange(xx, t+1)
		for xx in x.nested_type:
			lines+=self.genMessage(xx, t+1)
		for xx in x.field:
			lines+=self.genField(xx, t+1)
		if not (x.enum_type or x.nested_type or x.field):
			lines+=["%s\tpass"%("\t"*t)]
		return lines+[""]
	def genMethod(self, x, t=0):
		return [
			"%s@remote.method('%s', '%s')"%("\t"*t, x.input_type[1:], x.output_type[1:]),
			"%sdef %s(self, request):"%("\t"*t, x.name),
			"%s\treturn self.implementation.%s(request) "%("\t"*t, x.name),
			"",
		]
	def genService(self, x, t=0):
		lines=[
			"%sclass %s(remote.Service):"%("\t"*t, x.name),
			'%s\t"""'%("\t"*t),
			'%s\tUsage:'%("\t"*t),
			'%s\t\trpc_service_handlers = service_handlers.service_mapping(['%("\t"*t),
			"%s\t\t\t('/%s', %s.new_factory(implementation=%sImpl(parameters...)),"%("\t"*t, x.name, x.name, x.name),
			'%s\t\t])'%("\t"*t),
			'%s\t\t'%("\t"*t),
			'%s\t\t...then implement %sImpl accordingly:'%("\t"*t, x.name),
			'%s\t\t'%("\t"*t),
			'%s\t\tfrom rpc_services.hello import HelloRequest, HelloResponse, HelloService'%("\t"*t),
			'%s\t\tclass HelloServiceImpl(object):'%("\t"*t),
			'%s\t\t\tdef __init__(self, template):'%("\t"*t),
			'%s\t\t\t\tself.template = template'%("\t"*t),
			'%s\t\t\tdef hello(self, request):'%("\t"*t),
			'%s\t\t\t\treturn HelloResponse(hello=self.template%%request.my_name)'%("\t"*t),
			'%s\t\t'%("\t"*t),
			'%s\t"""'%("\t"*t),
			"%s\tdef __init__(self, implementation):"%("\t"*t),
			"%s\t\tself.implementation = implementation"%("\t"*t),
			"",
		]
		for xx in x.method:
			lines+=self.genMethod(xx, t+1)
		return lines
	def genFile(self, x, response):
		lines=[]
		if not x.package in self.created_files:
			lines+=[
				"#/usr/env/bin python",
				"from protorpc import messages, remote",
				"package='%s'"%x.package,
				""
			]
		lines+=["# Generated from %s" % x.name, ""]
		for xx in x.enum_type:
			lines+=self.genEnum(xx)
		for xx in x.extension:
			lines+=self.genExtension(xx)
		for xx in x.message_type:
			lines+=self.genMessage(xx)
		for xx in x.service:
			lines+=self.genService(xx)
		service_py=response.file.add()
		service_py.name='gen_rpc_services/%s.py'%x.package
		if x.package in self.created_files:
			service_py.insertion_point = "END"
		else:
			lines+=["# @@protoc_insertion_point(END)"]
			self.created_files[x.package]=True
		service_py.content='\n'.join(lines)
	def generate(self, request, response):
		m=response.file.add()
		m.name='gen_rpc_services/__init__.py'
		m.content=''
		for i in range(0, len(request.proto_file)):
			self.genFile(request.proto_file[i], response)
