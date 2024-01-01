-----------------------------------------------------------------------
-- {operator_name}, version 0.0
-----------------------------------------------------------------------

Library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.customTypes.all;

entity {dynamatic_name} is
Generic (
 INPUTS: integer; OUTPUTS: integer; DATA_SIZE_IN: integer; DATA_SIZE_OUT: integer
);
port (
  clk : IN STD_LOGIC;
  rst : IN STD_LOGIC;
  pValidArray : IN std_logic_vector(1 downto 0);
  nReadyArray : in std_logic_vector(0 downto 0);
  validArray : out std_logic_vector(0 downto 0);
  readyArray : OUT std_logic_vector(1 downto 0);
  dataInArray : in data_array (1 downto 0)(DATA_SIZE_IN-1 downto 0);
  dataOutArray : out data_array (0 downto 0)(DATA_SIZE_OUT-1 downto 0));
end entity;

architecture arch of {dynamatic_name} is
    {main_component}

    signal join_valid : STD_LOGIC;

    signal buff_valid, oehb_valid, oehb_ready : STD_LOGIC;
    signal oehb_dataOut, oehb_datain : std_logic_vector(0 downto 0);

    --intermediate input signals for float conversion
    {intermediate_input}

    --intermidiate output signal(s) for float conversion
    {intermediate_output}

    {additional_signals}

    begin


        join: entity work.join(arch) generic map(2)
        port map( pValidArray,
                oehb_ready,
                join_valid,
                readyArray);

        {buffer}

        oehb: entity work.OEHB(arch) generic map (1, 1, 1, 1)
                port map (
                --inputspValidArray
                    clk => clk,
                    rst => rst,
                    pValidArray(0)  => buff_valid, -- real or speculatef condition (determined by merge1)
                    nReadyArray(0) => nReadyArray(0),
                    validArray(0) => validArray(0),
                --outputs
                    readyArray(0) => oehb_ready,
                    dataInArray(0) => oehb_datain,
                    dataOutArray(0) => oehb_dataOut
                );

        {ieee2nfloat_0}

        {ieee2nfloat_1}

        {bit_flip_instance}

        {nfloat2ieee}

        operator :  component {operator_name}
        port map (
            clk   => clk and oehb_ready,
            X  => X_in,
            Y  => Y_in,
            R  => R_out
        );
end architecture;

