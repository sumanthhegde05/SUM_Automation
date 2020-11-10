*** Settings ***
Library     OperatingSystem
Library     String
Library     Process
Library     Selenium2Library    timeout=20  run_on_failure=Nothing
Library     Python_files\\ping.py
Library     Python_files\\kill.py
Library     Python_files\\ssh.py
Library     Python_files\\clear.py

#Suite Teardown      run keyword if any tests failed     end

*** Variables ***
${compare}=  yes
${spp_dir_name}  
${custom_baseline_path}     
${spp_drive_path}
${selected}
${total}
${flag}=   True
${day}
${output_path}
*** Test Cases ***
Test Initialize  
    @{date}  Get Time  year day month
    @{time}  Get Time  hour min sec

    FOR  ${item}  IN RANGE  0  3
        ${val2}=    Evaluate    2-${item}
        set global variable  ${day}  ${day}@{date}[${val2}]_
    END
    FOR  ${item}  IN RANGE  0  3
        set global variable  ${day}  ${day}@{time}[${item}]_ 
    END
    log to console  Times stamp : ${day}

    run keyword if  '${input}'=='no'  set global variable  ${flag}  False
    run keyword if  '${input}'=='no'  log to cosole  Input file found at "${input_file}"
    run keyword if  ${flag}==True  log to console  UI has been enabled. Input file found at "<path to script>\\Text_files\\input.txt"
    run keyword if  ${flag}==True  run process  python  Python_files\\ui.py 
    run keyword if  ${flag}==True  set global variable  ${input_file}  Text_files\\input.txt
    ${file}=    get file    ${input_file}    encoding=UTF-8
    @{lines}=   split to lines  ${file}

    FOR  ${node_line}  IN  @{lines}
        ${node}  Split String	 ${node_line}  ${SPACE}
        run keyword if  '${node}[0]'=='SPP_ISO='   set global variable   ${spp_dir_name}   ${node}[1]  
        run keyword if  '${node}[0]'=='CUSTOM_BASELINE_DIR='   set global variable     ${custom_baseline_path}     ${node}[1]
        run keyword if  '${node}[0]'=='CD_DRIVE='   set global variable    ${spp_drive_path}     ${node}[1]
        run keyword if  '${node}[0]'=='OUTPUT_PATH='   set global variable   ${output_path}   ${node}[1] 
    END
    log to console  Spp directory : ${spp_dir_name}
    log to console  Custom baseline : ${custom_baseline_path}
    log to console  output file : ${output_path}
    log to console  Cd drive : ${spp_drive_path}
    
    create file  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\Details\\dash.txt
    run process  python  Python_files\\config.py  ${input_file}

    :For    ${var}  IN RANGE    5
    \   ${ping_result}  ping status  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\Details\\dash.txt
    \   log to console  Ping successfully : ${ping_result}
    \   run keyword if  '${ping_result}' != '${compare}'  set global Variable  ${flag}  True
    \   continue for loop if  '${ping_result}' != '${compare}'
    \   ${ssh_result}  ssh reply  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\Details\\dash.txt
    \   log to console  Ssh successfully : ${ssh_result}
    \   run keyword if  '${ssh_result}' != '${compare}'  set global Variable  ${flag}  True
    \   exit for loop if  '${ssh_result}' == '${compare}'

    ${size}  Get File Size   Text_files\\user.txt
    run keyword if  ${size} == 0 log to console  No nodes were valid
    run keyword if  ${size} == 0 Fatal Error

    Test main

*** Keywords ***
Test main
    close all browsers
    create file     ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\Details\\baseline_error.txt
    ${file}=    get file    Text_files\\user.txt    encoding=UTF-8
    @{lines}=   split to lines  ${file}
    FOR  ${node_line}  IN  @{lines}
        log to console  ............................${node_line}.......................................
        ${start_condition}  run keyword and ignore error  Test Start
        continue for loop if  '${start_condition}[0]'=='FAIL'
        log to console  Browser launch was successful.
    ###################################################################################################################
        ${node}=	Split String	${node_line}	    ${SPACE}
        Set Screenshot Directory    ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\${node}[0]\\screenshots
    ###################################################################################################################
        ${baseline_condition}  run keyword and ignore error   Test Baseline
        run keyword if  '${baseline_condition}[0]'=='FAIL'  Test Main Error  Baseline_Addition_Failed  ${node}
        run keyword if  '${baseline_condition}[0]'=='FAIL'  capture page screenshot
        continue for loop if  '${baseline_condition}[0]'=='FAIL'
        log to console  Baseline added successfully.
    ###################################################################################################################
        ${add_node_condition}  run keyword and ignore error  Test Addnode   ${node}
        run keyword if  '${add_node_condition}[0]'=='FAIL'  capture page screenshot
        run keyword if  '${add_node_condition}[0]'=='FAIL'  Test Main Error  Node_Addition_Failed  ${node}
        continue for loop if  '${add_node_condition}[0]'=='FAIL'
        log to console  Node ${node_line} successfully added.
    ###################################################################################################################
        ${inventory_condition}  run keyword and ignore error  Test Inventory
        run keyword if  '${inventory_condition}[0]'=='FAIL'  Test Main Error  Inventory_Failed  ${node}
        run keyword if  '${inventory_condition}[0]'=='FAIL'  capture page screenshot
        continue for loop if  '${inventory_condition}[0]'=='FAIL'
        log to console  Node ${node_line} inventory successful.
    ###################################################################################################################
        ${deployment_condition}  ${selected}  run keyword and ignore error  Test Deployment  ${node}
        run keyword if  '${deployment_condition}'=='FAIL'  Test Main Error  Deployment_Failed  ${node}
        run keyword if  '${deployment_condition}'=='FAIL'  capture page screenshot
        continue for loop if  '${deployment_condition}[0]'=='FAIL'
        log to console  Node ${node_line} ${selected} components deployment successful.
    ###################################################################################################################
        ${log_condition}  ${ip_name}  run keyword and ignore error  Test Log  ${selected}
        run keyword if  '${log_condition}'=='PASS'  run keyword and ignore error  Test End  ${ip_name}
        run keyword if  '${log_condition}'=='FAIL'  Test Main Error  Log_Failed  ${node}
        run keyword if  '${log_condition}'=='FAIL'  capture page screenshot
        log to console  Node ${node_line} logs collected successful.
    ###################################################################################################################
        sleep  30
        clearall
        sleep  10
    END

    run process  python  Python_files\\dashboard.py  ${output_path}\\${spp_dir_name}\\${day}


Test Start    
    FOR  ${inc}  IN RANGE  5
        kill cmd
        close all browsers
        run process  python  Python_files\\remove.py
        sleep  2 
        ${launch_status}  Run keyword and return status  Test Launch
        log to console  Trial ${inc} : Web browser launch successful : ${launch_status}
        exit for loop if    ${launch_status}==True
        sleep  3
    END
    run keyword if  ${launch_status}==False  FAIL


Test Launch
    start process  launch_sum.bat  shell=true  cwd=${spp_drive_path}\\
    sleep  1 min
    run process  Taskkill /F /IM firefox.exe  shell=True
    sleep  2
    open browser  https://localhost:63002/index.html  ff
    maximize browser window
    #wait until page contains    Advanced    timeout=5
    #click button    Advanced
    #sclick link     Proceed to localhost (unsafe)
    wait until page contains  Login  timeout=10
    input text  xpath://input[@id='hp-login-user']  Administrator
    input text  xpath://input[@id='hp-login-password']  Hptc_ib
    click element  xpath://button[@id='hp-login-button']


Test Baseline
    log to console  Baseline test has been started.
    Set Selenium Implicit Wait  20
    wait until page contains  Baseline  timeout=5
    click element  xpath://li[@id='select-baseline']//div[@class='hp-home-ico']
    ${baseline_addition_status}  run keyword and ignore error  wait until element contains  xpath://header[@class='hp-notification-summary']  Baseline successfully added
    run keyword if  '${baseline_addition_status}[0]' == 'FAIL'  Test Baseline Continue
    ${custom_baseline_addition_status}  run keyword if  '${custom_baseline_path}'!='None'  run keyword and ignore error  Test Custom Baseline
    run keyword if  '${custom_baseline_addition_status}'=='FAIL'  FAIL
    go back


Test Baseline Continue
    wait until page contains  Add Baseline  timeout=5
    click element  xpath://a[@id='hpsum-add-baselinebtn']
    wait until page contains  Add  timeout=5
    click element  xpath://a[@id='hpsum-action-addbaseline']
    wait until page contains  Browse  timeout=5
    click element  xpath://input[@id='hpsum-baseline-add-browse-hpsumBrowse-browse-button']
    click element  xpath://div[@id='browse']//ul
    sleep  1
    click element  xpath:/html[1]/body[1]/div[2]/div[8]/div[1]/div[1]/section[1]/div[1]/form[1]/div[1]/div[2]/ul[1]/li[2]/ul[1]/li[7]/a[1]
    wait until page contains  OK  timeout=5
    click element  xpath://input[@id='hpsum-browse-dialog-ok']
    wait until page contains  Add  timeout=5
    click element  xpath://input[@id='hpsum-baselines-add']
    wait until page contains  Service Pack for ProLiant  timeout=20
    wait until page contains  Smart Update Manager
    sleep  10
    FOR  ${inc}  IN RANGE  3
        sleep   2
        go back
    END


Test Custom Baseline
    wait until page contains  Add Baseline  timeout=5
    click element  xpath://a[@id='hpsum-add-baselinebtn']
    wait until page contains  Add  timeout=5
    click element  xpath://a[@id='hpsum-action-addbaseline']
    input text  xpath://input[@id='hpsum-baseline-add-browse-hpsumBrowse-input-text']  ${custom_baseline_path}
    wait until page contains  Add  timeout=5
    click element  xpath://input[@id='hpsum-baselines-add']
    ${error_check}  run keyword and ignore error  wait until page contains  Baseline has component warnings  timeout=30
    run keyword if  '${error_check}[0]'=='PASS'  Test Custom Baseline Error
    run keyword if  '${error_check}[0]'=='PASS'  FAIL
    wait until page contains  Smart Update Manager
    sleep  10
    FOR  ${inc}  IN RANGE  4
        sleep  2
        go back
    END


Test Addnode
    [Arguments]  ${node}
    log to console  Adding node.
    sleep  5
    wait until page contains  Nodes  timeout=10
    click element  xpath://li[@id='select-node']//div[@class='hp-home-ico']
    sleep  2
    click element  xpath://a[@class='hp-button hp-secondary']
    sleep  2
    input text  xpath://input[@id='hpsum-node-name']  ${node}[0]
    click element  xpath://a[@class='selectBox hp-select selectBox-dropdown']
    wait until page contains  Linux
    run keyword if  '${node}[3]'=='Windows'  click element  xpath://a[contains(text(),'Windows')]
    run keyword if  '${node}[3]'=='Linux'  click element  xpath://a[contains(text(),'Linux')]
    run keyword if  '${node}[3]'=='iLO-ESXi'  click element   xpath://a[contains(text(),'iLO')]
    sleep  2
    run keyword and ignore error    click element   xpath://input[@id='hpsum-node-replace']
    click element  xpath://div[@id='hpsum-node-edit-baseline-list']//div[@class='hp-search-combo-control']
    click element  xpath://div[@class='hp-search-combo-menu']
    sleep  2
    input text  xpath://input[@id='hpsum-node-add-baselines-search-input']  Service
    click element  xpath://div[@class='hp-search-combo-menu']//li
    run keyword if  '${custom_baseline_path}'!='None'  input text  xpath://input[@id='hpsum-node-add-hotfix-search-input']  ad
    run keyword if  '${custom_baseline_path}'!='None'  sleep  2
    run keyword if  '${custom_baseline_path}'!='None'  click element  xpath://div[@class='hp-search-combo hp-active']//li
    run keyword if  '${custom_baseline_path}'!='None'  click element  xpath://div[@id='hpsum-node-edit-baseline-list']//div[@class='hp-close']
    input text  xpath://input[@type='text'][@id='hpsum-node-credential-username']  ${node}[1]
    input text  xpath://input[@type='password'][@id='hpsum-node-credential-password']  ${node}[2]
    click button  Add
    sleep  2
    run keyword and ignore error  click button  Close


Test Inventory
    log to console  Inventory has been started.
    wait until page contains  Perform inventory  timeout=10 min
    click element  xpath://label[contains(text(),'Actions')]
    sleep  2
    wait until page contains  Inventory  timeout=10
    click element   xpath://a[@id='hpsum-node-action-inventory']
    sleep  2
    click button  Inventory
    create file  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\Details\\warnings.txt
    ${status}  ${warning}  run keyword and ignore error  get text  xpath://div[@id='hpsum-warning-messages']
    append to file  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\Details\\warnings.txt   During inventory \n ${warning} \n \n
    sleep  10 min
    ${inventory_status}  run keyword and ignore error  page should contain  Inventory failed
    run keyword if  '${inventory_status}[0]'=='PASS'  FAIL
    wait until page contains  Ready for deployment  timeout=30 min


Test Deployment
    [Arguments]  ${node}
    log to console  Deployment has been started
    ${status}  ${warning}  run keyword and ignore error  get text  xpath://div[@id='hpsum-warning-messages']
    run keyword and ignore error  capture element screenshot  xpath://div[@id='hpsum-warning-messages']
    append to file  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\Details\\warnings.txt  When ready for deployment \n ${warning}
    click element   xpath://a[contains(text(),'Review and deploy updates')]
    sleep  30
    run keyword and ignore error  click element  xpath://input[@class='useWEBEMcheckbox ignorewarnings']
    #run keyword if      '${node}[3]'=='iLO-ESXi'   Test Esxi
    click element  xpath://a[@id='show-reboot-details']
    sleep  2
    click element  xpath://ol[@id='hpsum-common-reboot-options']//span[@class='selectBox-arrow']
    sleep  2
    click element  xpath://a[contains(text(),'Always')]
    click element  xpath://input[@id='hpsum-deselectall-comp']
    run keyword if  '${node}[4]'!='All' and '${node}[4]'!='FW_All'  Test Selection  ${node}
    run keyword if  '${node}[4]'=='FW_All'  Test Firmware All
    run keyword if  '${node}[4]'=='All'  click element   xpath://input[@id='hpsum-selectall-comp'] 
    ${selected}  get text  xpath:/html[1]/body[1]/div[2]/div[4]/div[1]/div[1]/section[1]/form[1]/ol[1]/li[5]/div[1]/ol[1]/li[2]/ol[1]/li[1]/div[1]/ol[1]/div[1]/ol[1]/li[2]/div[1]/div[5]/b[1]/label[1]
    ${selected}  convert to integer  ${selected}
    log to console  Total selected components : ${selected}
    run keyword and ignore error  Append to file  Text_files\\result.txt  ${selected} \n  
    run keyword if  ${selected}==0  FAIL
    sleep  1 min
    click element  xpath://input[@id='hpsum-node-deploy-ok']
    [Return]  ${selected} 

Test Selection
    [Arguments]     ${node}
    sleep  1 min
    ${total_count}  get text  xpath:/html[1]/body[1]/div[2]/div[4]/div[1]/div[1]/section[1]/form[1]/ol[1]/li[5]/div[1]/ol[1]/li[2]/ol[1]/li[1]/div[1]/ol[1]/div[1]/ol[1]/li[2]/div[1]/div[3]/b[1]/label[1]
    ${total_count}  convert to integer  ${total_count}
    log to console  Total components found : ${total_count}
    Create File  Text_files\\result.txt
    ${search}  get file  Text_files\\search.txt  encoding=UTF-8
    @{key_words}  split to lines  ${search}
    FOR  ${search_elem}  IN  @{Key_words}
        @{item}  Split String  ${search_elem}  ${SPACE}
        continue for loop if  '@{item}[0]'=='#'
        continue for loop if  '${node}[3]'=='iLO-ESXi' and '@{item}[-1]'=='x64)'
        Search loop  ${search_elem}  ${total_count}  ${node}[4]
        sleep   5
    END

    ${matched_file}  get file  Text_files\\result.txt  encoding=UTF-8
    @{matched_list}  split to lines  ${matched_file}    
    FOR  ${val}  IN  @{matched_list}
        @{pos}  Split String  ${val}
        ${inc}  Convert to integer  @{pos}[0]
        click element  xpath:/html[1]/body[1]/div[2]/div[4]/div[1]/div[1]/section[1]/form[1]/ol[1]/li[5]/div[1]/ol[1]/li[2]/ol[1]/li[1]/div[1]/ol[1]/div[1]/ol[1]/li[2]/div[1]/div[6]/div[3]/table[1]/tbody[1]/tr[${inc}]/td[2]
        sleep  20
    END

Search loop
    [Arguments]  ${search_elem}  ${total_count}  ${component}
    log to console  ${search_elem} : ${component}
    FOR  ${inc}  IN RANGE  1  ${total_count}+5
        ${component_type_status}  Run Keyword If  '${component}'!='Both'  run keyword and return status  element should contain  xpath://li[@id='li-expert-mode-baseline-assocnodes']//tr[${inc}]//td[4]  ${component}
        run keyword if  '${component}'=='Both'   set test Variable   ${component_type_status}    True
        ${component_name_status}  run keyword and return status  element should contain      xpath://li[@id='li-expert-mode-baseline-assocnodes']//tr[${inc}]/td[2]     ${search_elem}
        ${slno}  Convert to String  ${inc}     
        log to console  component_type_status : ${component_type_status} component_name_status : ${component_name_status}
        run keyword if  ${component_name_status}==True and ${component_type_status}==True  Append To File  Text_files\\result.txt  ${slno} \n
    END


Test Firmware All
    Create File  Text_files\\result.txt
    sleep  1 min
    ${total_count}  get text  xpath:/html[1]/body[1]/div[2]/div[4]/div[1]/div[1]/section[1]/form[1]/ol[1]/li[5]/div[1]/ol[1]/li[2]/ol[1]/li[1]/div[1]/ol[1]/div[1]/ol[1]/li[2]/div[1]/div[3]/b[1]/label[1]       
    ${total_count}  convert to integer  ${total_count}
        log to console  total_count_${total_count}
    FOR  ${inc}  IN RANGE    1   ${total_count}+1
        ${fw_status}  run keyword and return status  element should contain  xpath://li[@id='hpsum-node-deploy-baselines']//tbody//tr[${inc}]//td[4]  Firmware
        ${slno}  Convert to String  ${inc}    
        run keyword if  ${fw_status}==True   Append To File     Text_files\\result.txt  ${slno} \n
        run keyword if  ${fw_status}==True   log to console  True
    END
    ${matched_file}  get file    Text_files\\result.txt  encoding=UTF-8
    @{matched_list}  split to lines  ${matched_file}    
    FOR  ${val}  IN  @{matched_list}
        @{pos}  Split String	${val}
        ${inc}  Convert to integer  @{pos}[0]
        click element  xpath:/html[1]/body[1]/div[2]/div[4]/div[1]/div[1]/section[1]/form[1]/ol[1]/li[5]/div[1]/ol[1]/li[2]/ol[1]/li[1]/div[1]/ol[1]/div[1]/ol[1]/li[2]/div[1]/div[6]/div[3]/table[1]/tbody[1]/tr[${inc}]/td[1]
        sleep  20
    END


Test Log
    [Arguments]  ${selected}
    ${ip_name}  get text  xpath:/html[1]/body[1]/div[2]/div[3]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[2]
    create file  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\${ip_name}\\result.txt
    create file  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\${ip_name}\\error.txt
    ${installation_status}  run keyword and ignore error  wait until page contains  Install done  timeout=75 min
    ${error_check}  run keyword if  '${installation_status}[0]'=='FAIL'  run keyword and return status  element should contain  xpath://header[@class='hp-notification-summary']  Deploy completed with errors.
    run keyword if  ${error_check}==True  Test Error  ${ip_name}
    run keyword if  ${error_check}==True  FAIL  Test not ready
    run keyword and ignore error  click element  xpath://a[@class='hp-button company-a']
    sleep  2
    run keyword and ignore error  click element  xpath://a[@class='hp-button']
    sleep  5
    set test variable  ${position}  0
    sleep  5
    :For  ${place_count}  IN RANGE  1  ${selected}+1
    \   sleep  10
    \   ${position}  Evaluate  ${position}+10
    \   log to console  pos_${position}
    \   Execute JavaScript    window.document.querySelector('div#hpsum-node-install-results-panel.hp-grid-panels.hp-grid-narrow').scrollTo(0,${position})
    \   run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[2]/div[4]/div[1]/div[1]/section[1]/form[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[${it}]/td[5]/a[1]
    \   ${name}  run keyword and ignore error     get text  xpath:/html[1]/body[1]/div[2]/div[4]/div[1]/div[1]/section[1]/form[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[${it}]/td[3]
    \   ${status}  ${result}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[2]/div[4]/div[1]/div[1]/section[1]/form[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[${it}]/td[4]
    \   ${entry}  run keyword and ignore error  Get value  xpath://textarea[@id='log-details']
    \   log to console  
    \   log to console  ${name}[1]
    \   run keyword if  '${name}[0]'=='PASS'  run keyword and ignore error  create File  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\${ip_name}\\${name}[1].txt
    \   run keyword if  '${name}[0]'=='PASS'  run keyword and ignore error  Append to file  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\${ip_name}\\result.txt  ${name}[1] : ${result} \n
    \   run keyword if  '${name}[0]'=='PASS'  run keyword and ignore error  Append to file  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\${ip_name}\\${name}[1].txt  ${entry}[1]
    \   run keyword if  '${name}[0]'=='PASS'  run keyword and ignore error  Append to file  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\Details\\dash.txt  ${ip_name}:${name}[1]:${result} \n

    [Return]  ${ip_name}


Test End
    [Arguments]     ${ip_name}
    sleep  5
    click element  xpath://input[@id='hpsum-node-install-results-close']
    sleep  5
    click element  xpath://label[contains(text(),'Actions')]
    sleep  10
    #click element   xpath://a[@id='hpsum-node-action-reboot']
    click element  xpath://li[@id='reboot-action-item']
    sleep  5
    click element  xpath://button[contains(text(),'Yes, Reboot')]
    kill cmd
    sleep  5
    create directory  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\${ip_name}\\gather_logs
    copy file  E:\\packages\\x64\\gatherlogs_x64.exe  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\${ip_name}\\gather_logs
    start Process  gatherlogs_x64.exe  shell=True  cwd=${output_path}\\${spp_dir_name}\\${day}\\output_logs\\${ip_name}\\gather_logs
    sleep  10
    close all browsers

Test Report
    [Arguments]  ${ip_name}
    Append To File  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\Details\\dash.txt  ${ip_name} - Deployment_Failed \n


Test Custom Baseline Error
    append to file  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\Details\\dash.txt  - - Baseline_addition_failed
    click element  xpath://a[@class='hp-anchor-uri']
    FOR  ${inc}  IN RANGE  1   999
        ${stst1}  ${val1}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[2]/div[3]/div[1]/div[2]/div[2]/section[1]/div[2]/section[1]/ol[1]/li[6]/div[2]/div[1]/table[1]/tbody[1]/tr[${inc}]/td[1]
        ${stat2}  ${val2}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[2]/div[3]/div[1]/div[2]/div[2]/section[1]/div[2]/section[1]/ol[1]/li[6]/div[2]/div[1]/table[1]/tbody[1]/tr[${inc}]/td[2]
        exit for loop if  '${stat1}'=='FAIL' or '${stat2}'=='FAIL'
        append to file  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\Details\\baseline_error.txt  ${val1} ${val2}
    END


Test Error
    [Arguments]  ${ip_name}
    ${content}  get text  xpath://header[@class='hp-notification-summary']
    append to file  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\${ip_name}\\error.txt  ${content}
    

Test Main Error
    [Arguments]  ${status}  ${node}    
    append to file  ${output_path}\\${spp_dir_name}\\${day}\\output_logs\\Details\\dash.txt  ${node}[0]:-:${status} \n

