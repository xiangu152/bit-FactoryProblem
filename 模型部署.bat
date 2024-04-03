@echo off
chcp 65001
setlocal
echo 开始部署模型
git clone https://github.com/xiangu152/bit-FactoryProblem.git
cd bit-FactoryProblem
git checkout master
xcopy /E /I /Y .\* ..\
cd ..
rmdir /S /Q bit-FactoryProblem
endlocal
echo 部署完成，按任意键退出
pause >nul
