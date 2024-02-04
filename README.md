local License = "KEYAUTH-vMXYDk-jqVEaB-ZWVkyH-iUZ3hn-Rdgir4-5HJHYN" --* Your License to use this script.

print(' KeyAuth Lua Example - https://github.com/mazk5145/')
local HttpService = game:GetService("HttpService")
local StarterGui = game:GetService("StarterGui")
local LuaName = "KeyAuth Lua Example"

StarterGui:SetCore("SendNotification", {
    Title = LuaName,
    Text = "Initializing Authentication...",
    Duration = 5
})

--* Configuration *--
local initialized = false
local sessionid = ""

--* Application Details *--
local name = "Xapj"
local ownerid = "MKS500Xxla"
local version = "1.0"

local initReq = game:HttpGet('https://keyauth.win/api/1.1/?name=' .. name .. '&ownerid=' .. ownerid .. '&type=init&ver=' .. version)

if initReq == "KeyAuth_Invalid" then 
    print("Error: Application not found.")

    StarterGui:SetCore("SendNotification", {
        Title = LuaName,
        Text = "Error: Application not found.",
        Duration = 3
    })

    return false
end

local initData = HttpService:JSONDecode(initReq)

if initData.success == true then
    initialized = true
    sessionid = initData.sessionid
else
    print("Error: " .. initData.message)
    return false
end

print("\n\nLicensing... \n")
local licenseReq = game:HttpGet('https://keyauth.win/api/1.1/?name=' .. name .. '&ownerid=' .. ownerid .. '&type=license&key=' .. License ..'&ver=' .. version .. '&sessionid=' .. sessionid)
local licenseData = HttpService:JSONDecode(licenseReq)

if licenseData.success == false then 
    StarterGui:SetCore("SendNotification", {
        Title = LuaName,
        Text = "Error: " .. licenseData.message,
        Duration = 5
    })

    return false
end

StarterGui:SetCore("SendNotification", {
    Title = LuaName,
    Text = "Successfully Authorized :)",
    Duration = 5
})

--* Your code here *--

--* Example Code to show user data *-- 
print('Logged In!')
print('User Data')
print('Username: ' .. licenseData.info.username)
print('IP Address: ' .. licenseData.info.ip)
print('Created at: ' .. licenseData.info.createdate)
print('Last login at: ' .. licenseData.info.lastlogin)
