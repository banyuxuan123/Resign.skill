@echo off
chcp 65001 >nul
REM Lark Handover Skill 安装脚本（Windows）

echo 🚀 开始安装 Lark Handover Skill...

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装，请先安装 Python 3.8+
    exit /b 1
)

for /f "tokens=2" %%a in ('python --version') do set PYTHON_VERSION=%%a
echo ✅ Python 版本: %PYTHON_VERSION%

REM 检查并安装 lark-cli
echo 📦 检查 lark-cli...
lark-cli --version >nul 2>&1
if errorlevel 1 (
    echo    安装 lark-cli...
    pip install lark-cli
) else (
    echo ✅ lark-cli 已安装
)

REM 创建 Skill 目录
set SKILL_DIR=%USERPROFILE%\.qwen\skills\lark-handover
echo 📁 创建 Skill 目录: %SKILL_DIR%

if not exist "%SKILL_DIR%" mkdir "%SKILL_DIR%"

REM 复制文件
echo 📂 复制文件...
xcopy /E /I /Y skills "%SKILL_DIR%\skills\" >nul
xcopy /E /I /Y scripts "%SKILL_DIR%\scripts\" >nul
xcopy /E /I /Y references "%SKILL_DIR%\references\" >nul
copy /Y SKILL.md "%SKILL_DIR%\" >nul
copy /Y README.md "%SKILL_DIR%\" >nul
copy /Y LICENSE "%SKILL_DIR%\" >nul
copy /Y pyproject.toml "%SKILL_DIR%\" >nul

echo.
echo ✨ 安装完成！
echo.
echo 📋 下一步：
echo    1. 运行: lark-cli auth login --no-wait --domain all
echo    2. 完成飞书授权
echo    3. 运行: python %SKILL_DIR%\scripts\generate_handover.py --user 你的姓名
echo.
echo 📖 查看文档: type %SKILL_DIR%\README.md
echo.

pause
