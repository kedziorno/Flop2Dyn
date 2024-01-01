--- Flips the msb of input, equivalent to fneg_op
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity FlipMSB is
    Generic (
        BIT_WIDTH : integer := 32  -- Default to 32 bits, can be overridden
    );
    Port (
        input_signal  : in  STD_LOGIC_VECTOR(BIT_WIDTH-1 downto 0);
        output_signal : out STD_LOGIC_VECTOR(BIT_WIDTH-1 downto 0)
    );
end FlipMSB;

architecture Behavioral of FlipMSB is
begin
    -- Process to flip the MSB of the input signal
    process(input_signal)
    begin
        output_signal <= not input_signal(BIT_WIDTH-1) & input_signal(BIT_WIDTH-2 downto 0);
    end process;

end Behavioral;
