Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class KerberosAuthenticator
{
[DllImport("advapi32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
public static extern bool LogonUser(string lpszUsername, string lpszDomain, string lpszPassword, int dwLogonType, int dwLogonProvider, out IntPtr phToken);

[DllImport("kernel32.dll", SetLastError = true)]
public static extern bool CloseHandle(IntPtr hObject);
}
"@

# Define an array of user credentials
$userList = @(
@{Domain = "garageproject01.com"; Username = "GPUSER011"; Password = "Pass@12345"},
@{Domain = "garageproject01.com"; Username = "GPUER02"; Password = "Pass@123456"},
@{Domain = "garageproject01.com"; Username = "user3"; Password = "password3"}
)

# Iterate over the user list
foreach ($user in $userList) {
$domain = $user.Domain
$username = $user.Username
$password = $user.Password

$logonType = 2 # Interactive logon
$logonProvider = 0 # Default logon provider

# Acquire a Kerberos ticket for the domain controller
$tokenPtr = [IntPtr]::Zero
$success = [KerberosAuthenticator]::LogonUser($username, $domain, $password, $logonType, $logonProvider, [ref]$tokenPtr)

# Check if the authentication was successful
if ($success) {
Write-Host "Kerberos authentication successful for user: $username"
Write-Host "---------------------------------"

# Close the token handle
$closeHandleReturnValue = [KerberosAuthenticator]::CloseHandle($tokenPtr)
} else {
$errorCode = [System.Runtime.InteropServices.Marshal]::GetLastWin32Error()
Write-Host "Kerberos authentication failed for user: $username"
Write-Host "Error code: $errorCode"
Write-Host "---------------------------------"
}
}