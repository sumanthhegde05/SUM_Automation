*** Settings ***
Library     OperatingSystem
Library     String
Library     Process
Library     Selenium2Library

*** Variables ***

*** Test Cases ***
Test main
    open browser    https://192.168.5.123     ff
    maximize browser window
    sleep  5
    select frame  id=appFrame
    #wait until page contains element  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]  timeout=1 min
    wait until element contains  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]  Local login name
    input text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[4]/div[1]/form[1]/fieldset[1]/div[1]/span[1]/input[1]  admin
    input text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[4]/div[1]/form[1]/fieldset[1]/div[2]/span[1]/input[1]  admin123
    sleep  5
    click element  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[4]/div[1]/form[1]/footer[1]/button[1]
    wait until page contains  Firmware
    click element  xpath:/html[1]/body[1]/div[4]/div[1]/div[1]/div[1]/div[1]/nav[1]/ul[1]/li[3]  
    wait until page contains  Installation
    click element  xpath:/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/article[1]/div[1]/article[1]/section[1]/div[1]/ul[1]/li[6]/a[1]
    run keyword and ignore error  Test frame
    click element  xpath:/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/article[1]/div[1]/article[1]/section[1]/div[1]/ul[1]/li[5]/a[1]
    run keyword and ignore error  Test frame
    click element  xpath:/html[1]/body[1]/div[4]/div[1]/div[1]/div[2]/article[1]/div[1]/article[1]/section[1]/div[1]/ul[1]/li[4]/a[1]
    run keyword and ignore error  Test frame
    close all browsers

    #click button  Log In

*** Keywords ***
Test frame
    sleep  10
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