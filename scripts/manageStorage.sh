#Requirements

#Script must be run from root of storage with sample struct
# ├───2013
# ├───2014
# ├───Addons
# │   └───1213
# │       ├───2877213
# │       │   └───Windows8
# │       │       ├───x64
# │       │       │   └───NEU
# │       │       └───x86
# │       │           └───NEU
# │       ├───2891804
# │       │   ├───Windows7
# │       │   │   ├───x64
# │       │   │   │   └───NEU
# │       │   │   └───x86
# │       │   │       └───NEU
# │       │   ├───Windows8
# │       │   │   ├───x64
# │       │   │   │   └───NEU
# │       │   │   └───x86
# │       │   │       └───NEU
# │       │   └───WindowsVista
# │       │       ├───x64
# │       │       │   └───NEU
# │       │       └───x86
# │       │           └───NEU
#...

#fuseiso must be installed and working (see http://web.archive.org/web/20130519124548/http://www.ubuntu-unleashed.com/2008/04/howto-mount-isos-in-ubuntu-easy-way.html)
#Driver MHDDFS must be installed
#Samba server must be run (script using /srv/samba/share/ path to place storage struct)
#Tested on Ubuntu with sudo

getIsoFiles()
{
	for yearFolder in $(find ./* -maxdepth 0 -type d)
	do
		cd $yearFolder

		for iso in $(find *.iso)
		do
			echo $PWD/$iso
		done

		cd ..
	done
}

getAddonFolders()
{
	for folder in $(find ./Addons/* -maxdepth 0 -type d)
	do
		currFolder=$PWD
		cd $folder

		echo $PWD

		cd $currFolder
	done
}

mountImages()
{
	for iso in ${!1}
	do
		filename="${iso##*/}"
		filename="${filename%.*}"
		if [ ! -d /media/$filename ]; then sudo mkdir /media/$filename; fi
		sudo fuseiso $iso /media/$filename
	done
}

getIsoMountPoints()
{
	for path in ${!1}
	do
		filename="${path##*/}"
		filename="${filename%.*}"
		echo /media/$filename
	done
}

takeTogather()
{
	for path in ${!1}
	do
		arg+="$path,"
	done
	echo $arg
}

files=$(getIsoFiles)
folders=$(getAddonFolders)
mountImages files[@]
mountPoints=$(getIsoMountPoints files[@])

arg=$(takeTogather mountPoints[@])
arg+=$(takeTogather folders[@])

sudo mhddfs "${arg%?}" /srv/samba/share/ -o allow_other

echo "Done"
