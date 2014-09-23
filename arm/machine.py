#=======================================================================
# machine.py
#=======================================================================

from pydgin.storage import RegisterFile
from pydgin.debug   import Debug, pad, pad_hex

#-----------------------------------------------------------------------
# State
#-----------------------------------------------------------------------
class State( object ):
  def __init__( self, memory, debug, reset_addr=0x400 ):
    #self.pc       = reset_addr
    self.rf       = ArmRegisterFile( num_regs=16 )
    self.mem      = memory

    self    .debug = debug
    self.rf .debug = debug
    self.mem.debug = debug

    self.rf[ 15 ]  = reset_addr

    # current program status register (CPSR)
    self.N    = 0b0      # Negative condition
    self.Z    = 0b0      # Zero condition
    self.C    = 0b0      # Carry condition
    self.V    = 0b0      # Overflow condition
    #self.J    = 0b0      # Jazelle state flag
    #self.I    = 0b0      # IRQ Interrupt Mask
    #self.F    = 0b0      # FIQ Interrupt Mask
    #self.T    = 0b0      # Thumb state flag
    #self.M    = 0b00000  # Processor Mode

    # other registers
    self.status        = 0
    self.ncycles       = 0
    # unused
    self.stats_en      = 0
    self.stat_ncycles  = 0

    # syscall stuff... TODO: should this be here?
    self.breakpoint = 0

  def fetch_pc( self ):
    return self.rf.regs[15]

#-----------------------------------------------------------------------
# ArmRegisterFile
#-----------------------------------------------------------------------
class ArmRegisterFile( RegisterFile ):
  def __init__( self, num_regs=16 ):
    RegisterFile.__init__( self, constant_zero=False, num_regs=num_regs )

  def __getitem__( self, idx ):
    if self.debug.enabled( "rf" ):
      print ':: RD.RF[%s] = %s%s' % (
                          pad( "%d" % idx, 2 ),
                          pad_hex( self.regs[idx] ),
                          '+ 8' if idx == 15 else ''),

    if idx == 15:
      return self.regs[15] + 8
    else:
      return self.regs[idx]



