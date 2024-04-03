@echo off
chcp 65001
setlocal
set folder=./model
if not exist "%folder%" (
    echo 检测到不存在model文件夹，开始创建model文件夹
    mkdir "%folder%"
    echo 创建model文件夹成功
)
endlocal
setlocal
cd model
set model1=a.mdl
set model2=b.mdl
set model3=c.mdl
if exist %model1% if exist %model2% if exist %model3% (
    echo 模型已经部署在本地
) else (
    echo 开始部署模型
    set target = www.baidu.com
)
endlocal
setlocal
echo 是否需要下载数据集 y or n
set /p input
if "%input%"=="y" || "%input%"=="Y" (
    set folder=./csvdata
    if not exist "%folder%" (
        echo 检测到不存在csvdata文件夹，开始创建csvdata文件夹
        mkdir "%folder%"
        echo 创建csvdata文件夹成功
    )
    echo 开始下载数据集
    set target=www.baidu.com
    echo 数据集下载完毕
)
endlocal
echo 按任意键退出
pause >nul