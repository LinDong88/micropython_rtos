from building import *
import rtconfig

# get current directory
cwd     = GetCurrentDir()
# The set of source files associated with this SConscript file.
src     = Glob('py/*.c')
src    += Glob('ports/rtt/*.c')
src    += Glob('ports/rtt/boards/*.c')
src    += Glob('ports/rtt/modules/machine/*.c')
src    += Glob('ports/rtt/modules/modmachine.c')
src    += Glob('shared/runtime/interrupt_char.c')
src    += Glob('shared/runtime/pyexec.c')
src    += Glob('shared/runtime/stdout_helpers.c')
src    += Glob('shared/readline/readline.c')
#src    += Glob('port/modules/*.c')
#src    += Glob('port/modules/machine/*.c')
#src    += Glob('port/modules/user/*.c')
#src    += Glob('lib/netutils/*.c')
#src    += Glob('lib/timeutils/*.c')
#src    += Glob('drivers/bus/*.c')
#src    += Glob('port/native/*.c')

path    = [cwd + '/']
path   += [cwd + '/ports/rtt']
path   += [cwd + '/ports/rtt/boards']
path   += [cwd + '/shared/runtime']
path   += [cwd + '/shared/readline']
#path   += [cwd + '/port/modules/machine']

LOCAL_CCFLAGS = ' -Wno-overflow'
LOCAL_CCFLAGS += ' -Wno-stringop-truncation'
LOCAL_CCFLAGS += ' -Wno-incompatible-pointer-types'
LOCAL_CCFLAGS += ' -Wno-implicit-function-declaration'
LOCAL_CCFLAGS += ' -Wno-format'
LOCAL_CCFLAGS += ' -Wno-int-conversion'

if rtconfig.CROSS_TOOL == 'gcc':
    LOCAL_CCFLAGS += ' -std=gnu99'
elif rtconfig.CROSS_TOOL == 'keil':
    LOCAL_CCFLAGS += ' --c99 --gnu'

group = DefineGroup('MicroPython', src, depend = ['LPKG_USING_MICROPYTHON'], CPPPATH = path, CFLAGS = LOCAL_CCFLAGS)

Return('group')
