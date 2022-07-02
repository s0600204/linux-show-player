#
# This file is intended for use on Windows (10) and reverts the changes
# made by its companion script.
#

$classname = 'lspfile'
$extension = '.lsp'

Push-Location -Path Registry::HKEY_CURRENT_USER\SOFTWARE\Classes

##
## Remove file extension definition
##
if (Test-Path -Path .\$extension) {
	RemoveItem -Path .\$extension -Recurse
}

##
## Remove the file "class"
##
if (Test-Path -Path .\$classname) {
	Remove-Item -Path .\$classname -Recurse
}

Pop-Location
