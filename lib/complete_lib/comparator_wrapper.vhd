-----------------------------------------------------------------------
-- fcmp oeq, version 0.0
-----------------------------------------------------------------------

Library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;

use work.customTypes.all;

entity fcmp_oeq_op is
Generic (
INPUTS:integer :=2; 
OUTPUTS:integer := 1; 
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

architecture arch of fcmp_oeq_op is

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
    -- constant alu_opcode : std_logic_vector(4 downto 0) := "00001";

    --intermediate input signals for float conversion
    signal X_in, Y_in : std_logic_vector(33 downto 0);
    signal unordered : std_logic;
    signal equal : std_logic;
    signal ordered_and_equal : std_logic;

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
    
    ordered_and_equal <= not unordered and equal;
    dataOutArray(0)(0) <= ordered_and_equal;

end architecture;

-----------------------------------------------------------------------
-- fcmp ogt, version 0.0
-----------------------------------------------------------------------
Library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.customTypes.all;

entity fcmp_ogt_op is
Generic (
INPUTS:integer := 2; 
OUTPUTS:integer := 1; 
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

architecture arch of fcmp_ogt_op is

    component FloatingPointComparatorGT is
        port (
            clk, ce : in std_logic;
            X : in  std_logic_vector(33 downto 0);
            Y : in  std_logic_vector(33 downto 0);
            unordered : out  std_logic;
            XgtY : out  std_logic
            );
    end component;

    signal join_valid : STD_LOGIC;
    -- constant alu_opcode : std_logic_vector(4 downto 0) := "00010";
    signal X_in, Y_in : std_logic_vector(33 downto 0);
    signal unordered : std_logic;
    signal greater : std_logic;
    signal ordered_and_greater : std_logic;

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

    operator: FloatingPointComparatorGT
        port map (
            clk => clk,
            ce => nReadyArray(0),
            X => X_in,
            Y => Y_in,
            unordered => unordered,
            XgtY => greater
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
    
    ordered_and_greater <= not unordered and greater;
    dataOutArray(0)(0) <= ordered_and_greater;


end architecture;
-----------------------------------------------------------------------
-- fcmp oge, version 0.0
-- TODO
-----------------------------------------------------------------------
Library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.customTypes.all;

entity fcmp_oge_op is
    Generic (
    INPUTS:integer := 2;
    OUTPUTS:integer := 1;
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
    
architecture arch of fcmp_oge_op is

    component FloatingPointComparatorGE is
        port (
            clk, ce : in std_logic;
            X : in  std_logic_vector(33 downto 0);
            Y : in  std_logic_vector(33 downto 0);
            unordered : out  std_logic;
            XgeY : out  std_logic
            );
    end component;

    signal join_valid : STD_LOGIC;
    -- constant alu_opcode : std_logic_vector(4 downto 0) := "00011";
    signal X_in, Y_in : std_logic_vector(33 downto 0);
    signal unordered : std_logic;
    signal greater_or_equal : std_logic;
    signal ordered_and_greater_or_equal : std_logic;

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

    operator: FloatingPointComparatorGE
        port map (
            clk => clk,
            ce => nReadyArray(0),
            X => X_in,
            Y => Y_in,
            unordered => unordered,
            XgeY => greater_or_equal
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

    ordered_and_greater_or_equal <= not unordered and greater_or_equal;
    dataOutArray(0)(0) <= ordered_and_greater_or_equal;


end architecture;


-----------------------------------------------------------------------
-- fcmp olt, version 0.0
-- TODO
-----------------------------------------------------------------------
Library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.customTypes.all;

entity fcmp_olt_op is
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
    
architecture arch of fcmp_olt_op is

    component FloatingPointComparatorLT is
        port (
            clk, ce : in std_logic;
            X : in  std_logic_vector(33 downto 0);
            Y : in  std_logic_vector(33 downto 0);
            unordered : out  std_logic;
            XltY : out  std_logic
            );
    end component;

    signal join_valid : STD_LOGIC;
    -- constant alu_opcode : std_logic_vector(4 downto 0) := "00100";
    signal X_in, Y_in : std_logic_vector(33 downto 0);
    signal unordered : std_logic;
    signal less : std_logic;
    signal ordered_and_less : std_logic;

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

    operator: FloatingPointComparatorLT
        port map (
            clk => clk,
            ce => nReadyArray(0),
            X => X_in,
            Y => Y_in,
            unordered => unordered,
            XltY => less
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

    ordered_and_less <= not unordered and less;
    dataOutArray(0)(0) <= ordered_and_less;

end architecture;

-----------------------------------------------------------------------
-- fcmp ole, version 0.0
-- TODO
-----------------------------------------------------------------------

Library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.customTypes.all;
entity fcmp_ole_op is
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
    
    architecture arch of fcmp_ole_op is
    
        component FloatingPointComparatorLE is
            port (
                clk, ce : in std_logic;
                X : in  std_logic_vector(33 downto 0);
                Y : in  std_logic_vector(33 downto 0);
                unordered : out  std_logic;
                XleY : out  std_logic
                );
        end component;
    
        signal join_valid : STD_LOGIC;
        -- constant alu_opcode : std_logic_vector(4 downto 0) := "00101";
        signal X_in, Y_in : std_logic_vector(33 downto 0);
        signal unordered : std_logic;
        signal less_or_equal : std_logic;
        signal ordered_and_less_or_equal : std_logic;
    
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

    operator: FloatingPointComparatorLE
        port map (
            clk => clk,
            ce => nReadyArray(0),
            X => X_in,
            Y => Y_in,
            unordered => unordered,
            XleY => less_or_equal
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
    
    ordered_and_less_or_equal <= not unordered and less_or_equal;
    dataOutArray(0)(0) <= ordered_and_less_or_equal;
    
    end architecture;

-----------------------------------------------------------------------
-- fcmp one, version 0.0
-- TODO
-----------------------------------------------------------------------
Library IEEE;
use IEEE.std_logic_1164.all;
use ieee.numeric_std.all;
use work.customTypes.all;

entity fcmp_one_op is
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
    
    architecture arch of fcmp_one_op is
    
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
        signal ordered_and_not_equal : std_logic;

    
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

    ordered_and_not_equal <= not unordered and not equal;
    dataOutArray(0)(0) <= ordered_and_not_equal;
    
    end architecture;
