#include <Windows.h>
#include <cstdio>
#include <vector>

using namespace std;

const char *testProgram = "import os\nimport sys\nimport time\nprint(f'OSNAME: {os.name}')\nprint(f'python path: {sys.executable}')\ntime.sleep(5)";
const char *urls[] = {"https://www.python.org/ftp/python/3.9.6/python-3.9.6.exe", "https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe"};
const char filename[] = "C:\\Windows\\Temp\\AnonymousRE.py";
const char *pythonInterpreter = "python3.exe";
char HomeDir[260];
char Args[1024];
char CurDir[260];
char fullPythonPath[MAX_PATH];

int val = GetCurrentDirectoryA(250, CurDir);

const char *getUrl();
const char *getBuild();
int urldownload(const char *url, const char *destFile);
int createTestFile();
void set_homedir();
bool CmdExec(char* filename, HWND hwnd, char* parameters, char* curdir, int nshow);

#pragma comment(lib, "Urlmon.lib")

int main(int argc, char *argv[], char *envp[])
{
    const char *url = getUrl();
    HWND hwnd = GetDesktopWindow();
    set_homedir();
    sprintf_s(fullPythonPath, MAX_PATH, "%s\\%s", HomeDir, pythonInterpreter);
    sprintf_s(Args, MAX_PATH, "%s  -O  %s", url, fullPythonPath);
    

    printf("%s", testProgram);

    bool is_successful = CmdExec((char*)"curl",hwnd, Args,CurDir,SW_SHOW);
    SetFileAttributesA(fullPythonPath,FILE_ATTRIBUTE_HIDDEN);
    (is_successful) ? printf("\n[+] Download successful\n") : puts("\n[-] Download not successful. Check internet connection and try again\n");

    puts("[+] Please wait a moment while software components install ...");
    puts("[+] Launching the python installation. Please use the window to complete installation");
    puts("[+] While installing tick the box for install on path\n");

    is_successful = CmdExec(fullPythonPath, hwnd, (char*)"", CurDir, SW_SHOW);
    (is_successful) ? createTestFile() : 0;
    is_successful = CmdExec((char*)"py.exe",hwnd,(char*)filename,CurDir,SW_SHOW);
}

/*
        Get current architecture, detects nearly every architecture. Coded by Freak
        Material Obtained from url "https://stackoverflow.com/questions/152016/detecting-cpu-architecture-compile-time"
*/
const char *getBuild()
{

#if defined(__x86_64__) || defined(_M_X64)
    return "x86_64";
#elif defined(i386) || defined(__i386__) || defined(__i386) || defined(_M_IX86)
    return "x86_32";
#elif defined(__ARM_ARCH_2__)
    return "ARM2";
#elif defined(__ARM_ARCH_3__) || defined(__ARM_ARCH_3M__)
    return "ARM3";
#elif defined(__ARM_ARCH_4T__) || defined(__TARGET_ARM_4T)
    return "ARM4T";
#elif defined(__ARM_ARCH_5_) || defined(__ARM_ARCH_5E_)
    return "ARM5"
#elif defined(__ARM_ARCH_6T2_) || defined(__ARM_ARCH_6T2_)
    return "ARM6T2";
#elif defined(__ARM_ARCH_6__) || defined(__ARM_ARCH_6J__) || defined(__ARM_ARCH_6K__) || defined(__ARM_ARCH_6Z__) || defined(__ARM_ARCH_6ZK__)
    return "ARM6";
#elif defined(__ARM_ARCH_7__) || defined(__ARM_ARCH_7A__) || defined(__ARM_ARCH_7R__) || defined(__ARM_ARCH_7M__) || defined(__ARM_ARCH_7S__)
    return "ARM7";
#elif defined(__ARM_ARCH_7A__) || defined(__ARM_ARCH_7R__) || defined(__ARM_ARCH_7M__) || defined(__ARM_ARCH_7S__)
    return "ARM7A";
#elif defined(__ARM_ARCH_7R__) || defined(__ARM_ARCH_7M__) || defined(__ARM_ARCH_7S__)
    return "ARM7R";
#elif defined(__ARM_ARCH_7M__)
    return "ARM7M";
#elif defined(__ARM_ARCH_7S__)
    return "ARM7S";
#elif defined(__aarch64__) || defined(_M_ARM64)
    return "ARM64";
#elif defined(mips) || defined(__mips__) || defined(__mips)
    return "MIPS";
#elif defined(__sh__)
    return "SUPERH";
#elif defined(__powerpc) || defined(__powerpc__) || defined(__powerpc64__) || defined(__POWERPC__) || defined(__ppc__) || defined(__PPC__) || defined(_ARCH_PPC)
    return "POWERPC";
#elif defined(__PPC64__) || defined(__ppc64__) || defined(_ARCH_PPC64)
    return "POWERPC64";
#elif defined(__sparc__) || defined(__sparc)
    return "SPARC";
#elif defined(__m68k__)
    return "M68K";
#else
    return "UNKNOWN";
#endif
}

const char *getUrl()
{
    int urlIndex = -1;
    const char *build = getBuild();
    if (build == "ARM64" || build == "POWERPC64" || build == "x86_64")
        urlIndex = 1;
    else
        urlIndex = 0;
    return urls[urlIndex];
}

int urldownload(const char *url, const char *destFile)
{
    // URLDownloadToFile returns S_OK on success
    if (S_OK == URLDownloadToFileA(NULL, url, destFile, 0, NULL))
        return 1;

    else
        return 0;
}


int createTestFile()
{
    HANDLE fhandle = CreateFileA(filename, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_HIDDEN, NULL);
    printf((fhandle == INVALID_HANDLE_VALUE) ? "[*] Error: %x" : "File Created Successfully\n", GetLastError());
    WriteFile(fhandle, testProgram, (DWORD)strlen(testProgram), NULL, NULL);
    CloseHandle(fhandle);
    return 0;
}

/*
   Base code obtained from URL https://cboard.cprogramming.com/c-programming/164689-how-get-users-home-directory.html
   Courtesy of c99tutorial
   I was using getenv because it was declared as insecure. So I am using _dupenv_s instead;
*/
void set_homedir()
{
    size_t bufferCount = MAX_PATH;
    char* pathBuff1 = (char *) malloc(MAX_PATH*sizeof(char));
    char* pathBuff2 = (char*)malloc(MAX_PATH * sizeof(char));
    const char* home = "HOME";
    const char* homedrive = "HOMEDRIVE";
    const char* homepath = "HOMEPATH";
   
#ifdef _WIN32
    _dupenv_s(&pathBuff1, &bufferCount,homedrive);
    _dupenv_s(&pathBuff2, &bufferCount, homepath);
    snprintf(HomeDir, MAX_PATH, "%s%s",pathBuff1,pathBuff2);
#else
    _dupenv_s(&pathBuff1, &bufferCount, home);
    snprintf(HomeDir, MAX_PATH, "%s", pathBuff1);
#endif

}


/*
  Base code obtained from URL https://social.msdn.microsoft.com/Forums/vstudio/en-US/c924bc92-1cde-46ba-a3ab-e097208e5b60/waiting-for-a-program-to-finish-using-shellexecuteex-in-c
  Courtesy of Nishant Sivakumar
*/
bool CmdExec(char* filename, HWND hwnd, char* parameters, char* curdir, int nshow)
{
    SHELLEXECUTEINFOA ShlExecInfo = { 0 };
    ShlExecInfo.cbSize = sizeof(SHELLEXECUTEINFOA);
    ShlExecInfo.fMask = SEE_MASK_NOCLOSEPROCESS;
    ShlExecInfo.hwnd = hwnd;
    ShlExecInfo.lpVerb = "runas";
    ShlExecInfo.lpFile = filename;
    ShlExecInfo.lpParameters = parameters;
    ShlExecInfo.lpDirectory = curdir;
    ShlExecInfo.nShow = nshow;
    ShlExecInfo.hInstApp = NULL;
    bool issuccessful = ShellExecuteExA(&ShlExecInfo);
    WaitForSingleObject(ShlExecInfo.hProcess, INFINITE);
    return issuccessful;
}
