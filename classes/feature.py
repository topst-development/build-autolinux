import os
import datetime
import sys
sys.path.append(os.path.join(os.getcwd(), 'classes/features'))

import common

import inspect
LogLevel = False

def debug(*msg):
	if LogLevel:
		print(inspect.stack()[1][1:4], end=' ')
		print(msg)
    
class Feature:
	def check_core(self, core):
		debug('')
		if core == 'sub':
			flist = self.sflist
			eflist = self.esflist
		else:
			flist = self.mflist
			eflist = self.emflist

		return flist, eflist

	def check_date(self, date):
		debug('')
		tmpmflist = []
		tmpsflist = []
		tmpemflist = []
		tmpesflist = []
		sdkdate = datetime.datetime(int(date.split('/')[0]), int(date.split('/')[1]), int(date.split('/')[2]))
		for f in self.mflist:
			if f['date'][0] == "~":
				feadate = f['date'][1:].split('/')
				if sdkdate <= datetime.datetime(int(feadate[0]), int(feadate[1]), int(feadate[2])) :
					tmpmflist.append(f)
					tmpemflist.append(f['name'])
			elif f['date'][-1] == "~":
				feadate = f['date'][:-1].split('/')
				if sdkdate >= datetime.datetime(int(feadate[0]), int(feadate[1]), int(feadate[2])) :
					tmpmflist.append(f)
					tmpemflist.append(f['name'])
			elif "~" in f['date']:
				fsincedate = f['date'].split('~')[0].split('/')
				funtildate = f['date'].split('~')[1].split('/')
				if sdkdate >= datetime.datetime(int(fsincedate[0]), int(fsincedate[1]), int(fsincedate[2])) and \
					sdkdate <= datetime.datetime(int(funtildate[0]), int(funtildate[1]), int(funtildate[2])):
					tmpmflist.append(f)
					tmpemflist.append(f['name'])
			else:
				print(f['name'] +" Main-Feature Date Invalid.")
				sys.exit(1)

		for f in self.sflist:
			if f['date'][0] == "~":
				feadate = f['date'][1:].split('/')
				if sdkdate <= datetime.datetime(int(feadate[0]), int(feadate[1]), int(feadate[2])) :
					tmpsflist.append(f)
					tmpesflist.append(f['name'])
			elif f['date'][-1] == "~":
				feadate = f['date'][:-1].split('/')
				if sdkdate >= datetime.datetime(int(feadate[0]), int(feadate[1]), int(feadate[2])) :
					tmpsflist.append(f)
					tmpesflist.append(f['name'])
			elif "~" in f['date']:
				fsincedate = f['date'].split('~')[0].split('/')
				funtildate = f['date'].split('~')[1].split('/')
				if sdkdate >= datetime.datetime(int(fsincedate[0]), int(fsincedate[1]), int(fsincedate[2])) and \
					sdkdate <= datetime.datetime(int(funtildate[0]), int(funtildate[1]), int(funtildate[2])):
					tmpsflist.append(f)
					tmpesflist.append(f['name'])
			else:
				print(f['name'] +" Sub-Feature Date Invalid.")
				sys.exit(1)

		self.mflist = tmpmflist
		self.sflist = tmpsflist

		remove_emlist = []
		remove_eslist = []
		for fn in self.emflist:
			if fn not in tmpemflist:
				remove_emlist.append(fn)
		for fn in self.esflist:
			if fn not in tmpesflist:
				remove_eslist.append(fn)

		self.emflist = [x for x in self.emflist if x not in remove_emlist]
		self.esflist = [x for x in self.esflist if x not in remove_eslist]

	def check_dep(self, flist, dep):
		debug('')
		flist.append(self.chipset)
		dep_list = dep.split()
		if dep_list:
			for idx, dep in enumerate(dep_list):
				if idx % 2 == 0:
					if dep[0] == "!":
						if dep[1:] not in flist:
							dep_list[idx] = "True"
						else:
							dep_list[idx] = "False"
					else:
						if dep in flist:
							dep_list[idx] = "True"
						else:
							dep_list[idx] = "False"
				else:
					if dep == "&&":
						dep_list[idx] = "and"
					elif dep == "||":
						dep_list[idx] = "or"
			flist.remove(self.chipset)
			return (eval(",".join(dep_list).replace(","," ")))
		else:
			flist.remove(self.chipset)
			return True

	def modifyExtFeature(self, core, name, status):
		debug('')
		remove_emflist = []
		remove_esflist = []
		if core == 'sub':
			for f in self.mflist:
				if f['name'] == name:
					f['status'] = status
					if status:
						self.emflist.append(f['name'])
					else:
						remove_emflist.append(f['name'])

			self.emflist = [x for x in self.emflist if x not in remove_emflist]
		else:
			for f in self.sflist:
				if f['name'] == name:
					f['status'] = status
					if status:
						self.esflist.append(f['name'])
					else:
						remove_esflist.append(f['name'])
			self.esflist = [x for x in self.esflist if x not in remove_esflist]

	def enableFeature(self, core, name):
		debug('')
		tmpflist, tmpeflist = self.check_core(core)
		for f in tmpflist:
			if f['name'] == name:
				f['status'] = True
				tmpeflist.append(f['name'])
				if f['name'] in f['edep']:
					self.modifyExtFeature(core, f['name'], True)

	def disableFeature(self, core, name):
		debug('')
		remove_eflist = []
		tmpflist, tmpeflist = self.check_core(core)
		for f in tmpflist:
			if f['name'] == name:
				f['status'] = False
				remove_eflist.append(f['name'])
				if f['name'] in f['edep']:
					self.modifyExtFeature(core, f['name'], False)
			if name in f['dep']:
				if f['dep'][0] != "!":
					f['status'] = False
					remove_eflist.append(f['name'])
					if f['name'] in f['edep']:
						self.modifyExtFeature(core, f['name'], False)

		tmpeflist = [x for x in tmpeflist if x not in remove_eflist]

		if 'sub' in core:
			self.sflist = tmpflist
			self.esflist = tmpeflist
		else:
			self.mflist = tmpflist
			self.emflist = tmpeflist

	def getFeatureProperty(self, core, name, prop):
		debug('')
		tmpflist, tmpeflist = self.check_core(core)

		value = ''
		for f in tmpflist:
			if f['name'] == name:
				value = f[prop]
				break;
		return value

	def getFeatureList(self, core):
		debug('')
		retArray = []
		eflist = []

		tmpflist, tmpeflist = self.check_core(core)

		for f in tmpflist:
			if self.check_dep(tmpeflist, f['dep']):
				retArray.append([f['name'], f['status'], f['desc']])

		return retArray

	def getEnableFeatureList(self, core):
		debug('')
		if core == 'sub':
			return self.esflist
		else:
			return self.emflist

	def write_feature(self, path, bbdef, m, core, bv, sdk):
		debug('')
		tmpflist, tmpeflist = self.check_core(core)

		lolist = []
		bblist = []
		LO = 'local.conf'
		BB = 'bblayers.conf'
		cfpath = os.path.join(path, 'build/'+m+'/conf/')

		for f in tmpflist:
			if f['conf'] == LO:
				lolist.append(f)
			elif f['conf'] == BB:
				bblist.append(f)

		#modify local.conf
		with open(cfpath+LO, 'r') as lof:
			lines = lof.readlines()

		with open(cfpath+LO, 'w') as lof:
			for line in lines:
				flush = False
				for f in lolist:
					if f['name'] in line and f['ID'] in line:
						if '"'+f['name']+'"' == line.split()[2]:
							if f['status']:
								if line[0] == '#':
									lof.write(line.replace(line, line[1:]))
									flush = True
								else:
									pass
							else:
								if line[0] == '#':
									pass
								else:
									lof.write(line.replace(line, '#'+line))
									flush = True
				if not flush:
					lof.write(line)

		#modify bblayers.conf
		with open(cfpath+BB, 'r') as f:
			text = f.read()
		with open(cfpath+BB, 'r') as f:
			lines = f.readlines()

		addlines = []
		for f in bblist:
			if not f['name'] in text and f['status']:
				addlines.append('  '+path+bbdef+f['ID']+f['name']+' \\\n')

		dellayers = []
		for idx, line in enumerate(lines):
			for f in bblist:
				if f['name'] in line and not f['status']:
					dellayers.append(idx)
		for layer in reversed(dellayers):
			del lines[layer]

		with open(cfpath+BB, 'w') as bbf:
			for line in lines:
				bbf.write(line)
				if 'meta-poky' in line:
					for addline in addlines:
						bbf.write(addline)

	def __init__(self, chipset, sdkdate,  sdk = 'ivi', mainfeatures = [], subfeatures = [], loadMain = True, loadSub = True):
		debug('')
		self.chipset = chipset
		self.mflist = []
		self.sflist = []
		self.emflist = []
		self.esflist = []

		feature = __import__(sdk)

		#common
		MainFeatures = common.MainFeatures
		SubFeatures = common.SubFeatures
		#SDK Features
		MainFeatures += feature.MainFeatures
		SubFeatures += feature.SubFeatures

		for f in MainFeatures:
			if f not in self.mflist:
				self.mflist.append(f)
				if not loadMain:
					f['status'] = False
				if f['status']:
					if f['name'] not in self.emflist:
						self.emflist.append(f['name'])

		for f in SubFeatures:
			if f not in self.sflist:
				self.sflist.append(f)
				if not loadSub:
					f['status'] = False
				if f['status']:
					if f['name'] not in self.esflist:
						self.esflist.append(f['name'])

		# Date Compare
		if sdkdate == 'up-to-date':
			sdkdate = datetime.datetime.now().strftime('%Y/%m/%d')

		self.check_date(sdkdate)

		# Status Compare
		if mainfeatures:
			for fn, status in mainfeatures:
				for f in self.mflist:
					if f['name'] == fn:
						f['status'] = status
						if status and fn not in self.emflist:
							self.emflist.append(fn)
						elif not status and fn in self.emflist:
							self.emflist.remove(fn)

		if subfeatures:
			for fn, status in subfeatures:
				for f in self.sflist:
					if f['name'] == fn:
						f['status'] = status
						if status and fn not in self.esflist:
							self.esflist.append(fn)
						elif not status and fn in self.esflist:
							self.esflist.remove(fn)

		# Dependency Check
		for f in self.mflist:
			if f['status']:
				f['status'] = self.check_dep(self.emflist, f['dep'])
				if not f['status']:
					self.emflist.remove(f['name'])

		for f in self.sflist:
			if f['status']:
				f['status'] = self.check_dep(self.esflist, f['dep'])
				if not f['status']:
					self.esflist.remove(f['name'])
