-----------------------------------------------------------------------
-- fcmp une, version 0.0
-- TODO
-----------------------------------------------------------------------
Library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.customTypes.all;

entity fcmp_une_op is
    Generic (
        INPUTS: integer := 2;
        OUTPUTS: integer := 1;
        DATA_SIZE_IN: integer := 32;
        DATA_SIZE_OUT: integer := 1
    );
    port(
        clk, rst : in std_logic; 
        dataInArray : in data_array (1 downto 0)(DATA_SIZE_IN-1 downto 0); 
        dataOutArray : out data_array (0 downto 0)(DATA_SIZE_OUT-1 downto 0);      
        pValidArray : in std_logic_vector(1 downto 0);
        nReadyArray : in std_logic_vector(0 downto 0);
        validArray : out std_logic_vector(0 downto 0);
        readyArray : out std_logic_vector(1 downto 0));
    end entity;
    
    architecture arch of fcmp_une_op is
    
        component FloatingPointComparatorEQ is
            port (
                clk, ce : in std_logic;
                X : in  std_logic_vector(33 downto 0);
                Y : in  std_logic_vector(33 downto 0);
                unordered : out  std_logic;
                XeqY : out  std_logic
                );
        end component;
    
        signal join_valid : STD_LOGIC;
        -- constant alu_opcode : std_logic_vector(4 downto 0) := "00110";
        signal X_in, Y_in : std_logic_vector(33 downto 0);
        signal unordered : std_logic;
        signal equal : std_logic;
        signal unordered_or_not_equal : std_logic;

    
    begin 
    
        --TODO check with lana
    dataOutArray(0)(DATA_SIZE_OUT - 1 downto 1) <= (others => '0');

    ieee2nfloat_0: entity work.InputIEEE_32bit(arch)
                port map (
                    --input
                    X => dataInArray(0),
                    --output
                    R => X_in
                );

    ieee2nfloat_1: entity work.InputIEEE_32bit(arch)
                port map (
                    --input
                    X => dataInArray(1),
                    --output
                    R => Y_in
                );

    operator: FloatingPointComparatorEQ
        port map (
            clk => clk,
            ce => nReadyArray(0),
            X => X_in,
            Y => Y_in,
            unordered => unordered,
            XeqY => equal
        );

    join_write_temp:   entity work.join(arch) generic map(2)
            port map( pValidArray,  --pValidArray
                nReadyArray(0),     --nready                    
                      join_valid,         --valid          
                readyArray);   --readyarray 

    buff: entity work.delay_buffer(arch) 
    generic map(1)
    port map(clk,
             rst,
             join_valid,
             nReadyArray(0),
             validArray(0));

    -- Outputs 1, if numbers are not equal, or at least one of the 2 numbers is NaN
    unordered_or_not_equal <= unordered or not equal;
    dataOutArray(0)(0) <= unordered_or_not_equal;
    
    end architecture;
