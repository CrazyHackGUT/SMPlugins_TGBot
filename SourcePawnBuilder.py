import subprocess

class Plugin(object):
    def __init__(self, file, out, include_directories = []):
        cmd = ["./SPComp/application/spcomp"]
        for dir in include_directories:
            cmd.append("-i{}".format(dir))
        cmd.append("-o{}".format(out))
        cmd.append(file)

        Compiler = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        Compiler.wait()

        self.CmdResponse = ""
        for line in Compiler.stdout:
            self.CmdResponse = "{}{}".format(self.CmdResponse, line.decode("utf-8"))
        self.ExitCode = Compiler.returncode

"""
MyPlugin = Plugin(
    "/home/kruzya/Test.sp",
    "/home/kruzya/Test",
    [
        "/home/kruzya/TGSMBot/SPComp/core_includes/",   # SourceMod Core includes
        "/home/kruzya/TGSMBot/SPComp/shared_includes/"  # Shared includes from bot developer (like VIP Core, EmitSoundAny, etc.)
    ]
)

print(MyPlugin.CmdResponse)
print("SourcePawn Compiler returned exit code {}".format(MyPlugin.ExitCode))
"""
