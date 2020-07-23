*** Settings ***
Library     OperatingSystem
Library     String
Library     Process
Library     Selenium2Library  timeout=10  run_on_failure=Nothing
Library     Collections

*** Variables ***
@{content}
*** Test Cases ***
Test main
    ${file}=    get file    c:\\input.txt    encoding=UTF-8
    @{lines}=   split to lines  ${file}
    #log to console  ${lines}
    :For     ${elem}  IN   @{lines}
    \    ${word}  split string  ${elem}
    \    ${status1}  run keyword and ignore error  should contain  ${word}[0]  1
    \    ${status2}  run keyword and ignore error  should contain  ${word}[0]  \#
    \    continue for loop if  '${status1}[0]'=='FAIL' or '${status2}[0]'=='PASS'
    \    log to console  ${elem}
    \    ${address}  split string  ${word}[0]  .
    \    Test Launch  ${address}
    \    wait until page contains  Installation
    \    click element  xpath:/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/article[1]/div[1]/article[1]/section[1]/div[1]/ul[1]/li[6]/a[1]
    \    run keyword and ignore error  Test frame
    \    click element  xpath:/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/article[1]/div[1]/article[1]/section[1]/div[1]/ul[1]/li[5]/a[1]
    \    run keyword and ignore error  Test frame
    \    click element  xpath:/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/article[1]/div[1]/article[1]/section[1]/div[1]/ul[1]/li[4]/a[1]
    \    run keyword and ignore error  Test frame
    \    click element  xpath:/html[1]/body[1]/div[4]/div[1]/div[1]/div[1]/div[1]/nav[1]/ul[1]/li[6]/a[1]
    \    sleep  1
#    \    select frame  id=iframeContent
#    \    run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[4]/form[1]/div[1]/div[5]/div[2]/button[1]
#    \    run keyword and ignore error  xpath:/html[1]/body[1]/div[5]/div[1]/form[1]/table[1]/tbody[1]/tr[4]/td[2]/button[1]
    \    run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/article[1]/div[1]/article[1]/header[1]/a[1]/span[1]
    \    sleep  1
    \    run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/article[1]/div[1]/article[1]/header[1]/a[1]/div[1]/ul[1]/li[3]/a[1]
    \    sleep  2
#    \    unselect frame
#    \    select frame  id=appFrame
    \    click element  xpath:/html[1]/body[1]/div[9]/div[1]/div[3]/button[1]
    \    close all browsers
    
    #click button  Log In

*** Keywords ***
Test frame
    sleep  5
    ${status}  run keyword and ignore error  select frame  id=iframeContent
    wait until page contains  Remove all
    run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[5]/div[1]/div[1]/button[1]
    #run keyword and ignore error  click button  Remove all
    run keyword if  '${status}[0]'=='PASS'  unselect frame
    run keyword if  '${status}[0]'=='PASS'  select frame  id=appFrame
    run keyword and ignore error  wait until page contains  Yes, remove all
    run keyword and ignore error  click button  Yes, remove all
    run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[7]/div[2]/div[1]/div[1]/form[1]/footer[1]/button[1]
    sleep  5

Test Launch
    [Arguments]  ${address}
    :For  ${iter}   IN RANGE  0  5
    \    close all browsers
    \    ${status3}  run keyword and ignore error  loop  ${address}
    \    exit for loop if  '${status3}[0]'=='PASS'

loop
    [Arguments]  ${address}
    open browser    https://192.168.5.${address}[-1]   ff
    maximize browser window
    sleep  5
    select frame  id=appFrame
    wait until element contains  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]  Local login name
    input text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[4]/div[1]/form[1]/fieldset[1]/div[1]/span[1]/input[1]  admin
    input text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[4]/div[1]/form[1]/fieldset[1]/div[2]/span[1]/input[1]  admin123
    sleep  5
    click element  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[4]/div[1]/form[1]/footer[1]/button[1]
    sleep  5
    wait until page contains  Firmware
    click element  xpath:/html[1]/body[1]/div[4]/div[1]/div[1]/div[1]/div[1]/nav[1]/ul[1]/li[3]  