-- generated by pyha 0.0.4 at 2017-04-07 19:30:26
library ieee;
    use ieee.std_logic_1164.all;
    use ieee.numeric_std.all;
    use ieee.fixed_pkg.all;
    use ieee.math_real.all;

library work;
    use work.PyhaUtil.all;
    use work.ComplexTypes.all;
    use work.all;

entity  top is
    port (
        clk, rst_n, enable: in std_logic;

        -- inputs
        in0: in std_logic_vector(31 downto 0);

        -- outputs
        out0: out std_logic_vector(31 downto 0)
    );
end entity;

architecture arch of top is
begin
    process(clk, rst_n)
        variable self: Simple_0.self_t;
        -- input variables
        variable var_in0: integer;

        --output variables
        variable var_out0: integer;
    begin
	 
			 --convert slv to normal types
		var_in0 := to_integer(signed(in0));

		--call the main entry
		Simple_0.main(self, var_in0, ret_0=>var_out0);

		--convert normal types to slv
		out0 <= std_logic_vector(to_signed(var_out0, 32));
		
	 if (not rst_n) then
        Simple_0.reset(self);
    elsif rising_edge(clk) then
        if enable then
            Simple_0.update_registers(self);
        end if;
      end if;

    end process;
end architecture;