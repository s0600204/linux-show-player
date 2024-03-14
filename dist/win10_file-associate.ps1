#
# This file is intended for use on Windows (10) and does two things:
#
# 1. Set a file association for *.lsp files to open in Linux Show Player
#
# 2. Sets the icon for *.lsp files to use
#
# There exists a companion script that reverts the changes made in this
# script.
#

function New-SubPath {
	# Recursively creates the given subpath under the given path
	#
	# @todo: There must be a "proper" way of doing this. Find it; use it.

	param(
		[Parameter(Mandatory=$true)]
			[string]$Path,

		[Parameter(Mandatory=$true)]
			[string]$SubPath
	)

	Push-Location -Path $Path

	foreach ($segment in $SubPath.split("\"))
	{
		if (-not (Test-Path -Path .\$segment)) {
			New-Item     -Path .          -Name $segment
		}
		Set-Location -Path .\$segment
	}

	Pop-Location
}

Push-Location -Path Registry::HKEY_CURRENT_USER\SOFTWARE\Classes

$classname = 'lspfile'
$extension = '.lsp'

$iconname  = 'application-x-linuxshowplayer.ico'
$iconpath  = '%LOCALAPPDATA%\Programs\msys2\home\%USERNAME%\lisp\dist\'$iconname

$shell     = 'ucrt64'
$exepath   = '%LOCALAPPDATA%\Programs\msys2\'$shell'\bin\linux-show-player.exe'
$exeargs   = '-f "%1"'


##
## Define a file "class"
##
if (Test-Path -Path .\$classname) {
	Remove-Item -Path .\$classname -Recurse
}
New-Item      -Path .            -Name $classname
Push-Location -Path .\$classname

	# File Icon
	$iconkey = 'DefaultIcon'
	New-Item         -Path .          -Name $iconkey
	New-ItemProperty -Path .\$iconkey -Name '(Default)' -PropertyType ExpandString -Value $iconpath

	# Establish file association
	$subpath = 'shell\open\command'
	New-SubPath      -Path .          -SubPath $subpath
	New-ItemProperty -Path .\$subpath -Name '(Default)' -PropertyType ExpandString -Value $exepath $exeargs

Pop-Location


##
## Setup file extension
##
if (Test-Path -Path .\$extension) {
	RemoveItem -Path .\$extension -Recurse
}
New-Item      -Path .            -Name $extension
Push-Location -Path .\$extension

	# Use the above class, step 1 - Icon
	New-ItemProperty -Path . -Name '(Default)' -Value $classname

	# Use the above class, step 2  - File Association
	$openkey = 'OpenWithProgids'
	New-Item         -Path .          -Name $openkey
	New-ItemProperty -Path .\$openkey -Name $classname -PropertyType String -Value ''

Pop-Location


Pop-Location
