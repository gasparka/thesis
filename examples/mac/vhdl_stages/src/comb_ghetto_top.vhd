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

		type self_t is record
			mul: integer;
			acc: integer;
			coef: integer;
		end record;

		signal self: self_t := (mul=>0, acc=>0, coef=>123);

		procedure main(self: inout self_t; a: integer; ret_0: out integer) is
		begin
			self.mul := a * self.coef;
			self.acc := self.acc + self.mul;
			ret_0 := self.acc;
		end procedure;

begin

	process(clk)
		variable selfv: self_t;
		variable outp: integer;
	begin
		selfv := self;

		main(selfv, in0, outp);

		out0 <= outp;

		if rising_edge(clk) then
			self <= selfv;
		end if;

	end process;
end architecture;