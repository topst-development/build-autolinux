MainFeatures = [
	{
	 'name':'network',
	 'desc':'Install network packages',
	 'date':'2021/03/12~',
	 'status':True,
	 'conf':'local.conf',
	 'ID':'INVITE_PLATFORM',
	 'commercial':'',
	 'dep':'',
	 'edep':''
	},
	{
	 'name':'ssh-server-openssh',
	 'desc':'Install openssh with network packages',
	 'date':'2021/03/12~',
	 'status':True,
	 'conf':'local.conf',
	 'ID':'EXTRA_IMAGE_FEATURES',
	 'commercial':'',
	 'dep':'',
	 'edep':''
	},
	{
	 'name':'meta-micom',
	 'desc':'Enable Micom',
	 'date':'2020/07/17~',
	 'status':True,
	 'conf':'bblayers.conf',
	 'ID':'',
	 'commercial':'',
	 'dep':'tcc802x || tcc803x || tcc805x',
	 'edep':'meta-micom'
	},
	{
	 'name':'meta-update',
	 'desc':'Enable Update',
	 'date':'2020/03/02~',
	 'status':True,
	 'conf':'bblayers.conf',
	 'ID':'',
	 'commercial':'',
	 'dep':'',
	 'edep':'meta-update'
	},
]
SubFeatures = [
	{
	 'name':'meta-micom',
	 'desc':'Enable Micom',
	 'date':'2021/03/12~',
	 'status':True,
	 'conf':'bblayers.conf',
	 'ID':'',
	 'commercial':'',
	 'dep':'tcc802x || tcc803x || tcc805x',
	 'edep':'meta-micom'
	},
	{
	 'name':'meta-update',
	 'desc':'Enable Update',
	 'date':'2021/03/12~',
	 'status':True,
	 'conf':'bblayers.conf',
	 'ID':'',
	 'commercial':'',
	 'dep':'',
	 'edep':'meta-update'
	},
]
