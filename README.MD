# Use:
# https://github.com/hansalemaos/usefuladb
# https://github.com/hansalemaos/usefuladbplus


# Converts AndroidManifest.xml into a Pandas DataFrame (with all activities, queries, permissions ...)


```python

$pip install a-pandas-ex-adb-activities2df
# Install androguard
# git clone https://github.com/androguard/androguard.git
# pip install -r requirements.txt
# or pip: https://androguard.readthedocs.io/en/latest/intro/installation.html


from a_pandas_ex_adb_activities2df import connect_to_adb, list_all_packages,get_package_infos_df
import pandas as pd
adb_path = "C:\\Users\\Gamer\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"
deviceserial = "localhost:5895"
connect_to_adb(adb_path, deviceserial)
dfp_all_packages = list_all_packages(
    adb_path, deviceserial,
)  # returns a DataFrame with path and package name
dfp = dfp_all_packages.loc[
    dfp_all_packages.package_name.str.contains("roblox")
]  # filter here the packages you want to analyze
df, dfo = get_package_infos_df(
    dframe=dfp,  # Will analyze all packages in the DataFrame dfp
    adb_path=adb_path,
    deviceserial=deviceserial,
    tmp_folder_hdd="f:\\testdebugadb",  # Temp folder for apk files, folder will be created if it does not exist
    androguard_cli_py=r"C:\Users\Gamer\anaconda3\envs\dfdir\androguard\cli.py",  # https://github.com/androguard/androguard
    explode_name_columns=False,  # if True: might make it easier to find what you want, but the DataFrame will contain duplicated data
)
df1, dfo1 = get_package_infos_df(
    dframe=None,  # Will analyze all packages
    adb_path=adb_path,
    deviceserial=deviceserial,
    tmp_folder_hdd="f:\\testdebugadb",  # Temp folder for apk files, folder will be created if it does not exist
    androguard_cli_py=r"C:\Users\Gamer\anaconda3\envs\dfdir\androguard\cli.py",  # https://github.com/androguard/androguard
    explode_name_columns=False,  # if True: might make it easier to find what you want, but the DataFrame will contain duplicated data
)
 
 
 
                             package_path       package_name
7  /data/app/com.roblox.client-1/base.apk  com.roblox.client

dfp_all_packages

Out[6]: 
                                         package_path                     package_name
0   /data/priv-downloads/com.google.android.ext.se...  com.google.android.ext.services
1   /data/downloads/com.location.provider/com.loca...            com.location.provider
2   /system/priv-app/TelephonyProvider/TelephonyPr...  com.android.providers.telephony
3   /system/priv-app/CalendarProvider/CalendarProv...   com.android.providers.calendar
4    /system/priv-app/MediaProvider/MediaProvider.apk      com.android.providers.media
..                                                ...                              ...
65  /data/downloads/com.google.android.play.games/...    com.google.android.play.games
66  /data/downloads/gg.now.accounts/gg.now.account...                  gg.now.accounts
67    /system/app/WallpaperPicker/WallpaperPicker.apk      com.android.wallpaperpicker
68  /system/priv-app/ContactsProvider/ContactsProv...   com.android.providers.contacts
69  /system/app/CaptivePortalLogin/CaptivePortalLo...   com.android.captiveportallogin
[70 rows x 2 columns]



df
Out[13]: 
                                            aa_name_0  ... windowSoftInputMode_0
0                          android.intent.action.VIEW  ...                   NaN
1          com.roblox.client.landing.ActivityStartMVP  ...                    32
2                          android.intent.action.MAIN  ...                   NaN
3                com.roblox.client.ActivityNativeMain  ...                    16
4                 com.roblox.client.game.ActivityGame  ...                    16
5           com.roblox.client.game.GameLaunchActivity  ...                   NaN
6                 com.roblox.client.RobloxWebActivity  ...                   NaN
7        com.roblox.client.NotificationStreamActivity  ...                   NaN
8             com.roblox.client.signup.ActivitySignUp  ...                    32
9        com.roblox.client.login.mvp.ActivityLoginMVP  ...                   NaN
10  com.roblox.client.resetpassword.ResetPasswordA...  ...                   NaN
11        com.roblox.client.contacts.ActivityContacts  ...                   NaN
12  com.roblox.client.friends.ActivityUniversalFri...  ...                   NaN
13                   com.roblox.client.ActivitySearch  ...                   NaN
14       com.roblox.client.captcha.ActivityFunCaptcha  ...                   NaN
15  com.roblox.client.signup.multiscreen.ActivityV...  ...                    32
16  com.roblox.client.signup.multiscreen.ActivityW...  ...                   NaN
17            com.roblox.client.landing.AboutActivity  ...                   NaN
18  com.google.android.gms.auth.api.signin.interna...  ...                   NaN
19  com.google.android.gms.common.api.GoogleApiAct...  ...                   NaN
20  com.android.billingclient.api.ProxyBillingActi...  ...                   NaN
[21 rows x 31 columns]


dfo
Out[14]: 
                                               level_0  ...    aa_package_name
0                                          application  ...  com.roblox.client
1                                          application  ...  com.roblox.client
2                                          application  ...  com.roblox.client
3                                          application  ...  com.roblox.client
4                                          application  ...  com.roblox.client
..                                                 ...  ...                ...
164                                           uses-sdk  ...  com.roblox.client
165  {http://schemas.android.com/apk/res/android}co...  ...  com.roblox.client
166  {http://schemas.android.com/apk/res/android}co...  ...  com.roblox.client
167  {http://schemas.android.com/apk/res/android}ve...  ...  com.roblox.client
168  {http://schemas.android.com/apk/res/android}ve...  ...  com.roblox.client
[169 rows x 12 columns]


df1
Out[11]: 
                                              aa_name_0  ... windowSoftInputMode_0
0                            android.intent.action.MAIN  ...                   NaN
1                   com.location.provider.EnterLocation  ...                   NaN
2                com.location.provider.ShowMapsActivity  ...                   NaN
3                com.location.provider.BasicMapActivity  ...                   NaN
4     com.google.android.gms.common.api.GoogleApiAct...  ...                   NaN
                                                 ...  ...                   ...
1397                    android.net.conn.CAPTIVE_PORTAL  ...                   NaN
1398                                                NaN  ...                   NaN
1399                                                NaN  ...                   NaN
1400  com.android.captiveportallogin.CaptivePortalLo...  ...                   NaN
1401                                                NaN  ...                   NaN
[1402 rows x 227 columns]

dfo1
Out[15]: 
                                                 level_0  ... level_7
0                                            application  ...     NaN
1                                            application  ...     NaN
2                                            application  ...     NaN
3                                            application  ...     NaN
4                                            application  ...     NaN
                                                  ...  ...     ...
12107                                    uses-permission  ...     NaN
12108                                           uses-sdk  ...     NaN
12109                                           uses-sdk  ...     NaN
12110  {http://schemas.android.com/apk/res/android}ve...  ...     NaN
12111  {http://schemas.android.com/apk/res/android}ve...  ...     NaN
[12112 rows x 12 columns]


```
