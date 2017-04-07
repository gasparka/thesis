entity  top is
    port (
        in0: in integer;
        out0: out integer
    );
end entity;

architecture arch of top is

    function main(a: integer) return integer is
		variable mul, acc: integer;
    begin
        mul := 123 * a;
        acc := acc + mul;
        return acc;
    end function;
	 
begin
	 out0 <= main(in0);
end architecture;


library ieee;
	 use ieee.std_logic_1164.all;
	 use ieee.numeric_std.all;

entity  top is
    port (
		  clk: in std_logic;
        in0: in integer;
        out0: out integer
    );
end entity;

architecture arch of top is

    function main(a: integer) return integer is
		variable mul, acc: integer;
    begin
        mul := 123 * a;
        acc := acc + mul;
        return acc;
    end function;

begin
    process(clk)
    begin

		if rising_edge(clk) then
            out0 <= main(in0);
      end if;

    end process;

end architecture;