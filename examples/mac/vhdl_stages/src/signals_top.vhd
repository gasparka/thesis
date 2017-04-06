library ieee;
	 use ieee.std_logic_1164.all;
	 use ieee.numeric_std.all;
		 
entity  top is
    port (
		clk, rst_n: in std_logic;
        in0: in integer;
        out0: out integer
    );
end entity;

architecture arch of top is

		type next_t is record
			mul: integer;
			acc: integer;
		end record;

		type self_t is record
			mul: integer;
			acc: integer;
			nxt: next_t;
		end record;
		
		signal self: self_t := (mul=>0, acc=>0, nxt=>(mul=>0, acc=>0));
		
		procedure main(self: inout self_t; a: integer; ret_0: out integer) is
		begin
			self.nxt.mul := 123 * a;
			self.nxt.acc := self.acc + self.mul;
			ret_0 := self.acc;
		end procedure;
		
		procedure update_register(self: inout self_t) is
		begin
			self.mul := self.nxt.mul;
			self.acc := self.nxt.acc;
		end procedure;
	 
begin
	process(clk, rst_n)
		variable selfv: self_t;
		variable outp: integer; 
	begin
		selfv := self;
		
		main(selfv, in0, outp);
		
		out0 <= outp;
		if (not rst_n) then
			self <= (mul=>0, acc=>0, nxt=>(mul=>0, acc=>0));
		elsif rising_edge(clk) then
			update_register(selfv);
			self <= selfv;
		end if;

	end process;
end architecture;