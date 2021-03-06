-- generated by pyha 0.0.4 at 2017-04-01 22:23:31
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
        in0: in std_logic_vector(17 downto 0);

        -- outputs
        out0: out std_logic_vector(17 downto 0)
    );
end entity;

architecture arch of top is
begin
    process(clk, rst_n)
        variable self: DCRemoval_0.self_t;
        -- input variables
        variable var_in0: sfixed(0 downto -17);

        --output variables
        variable var_out0: sfixed(0 downto -17);
    begin
    if (not rst_n) then
        DCRemoval_0.\_pyha_reset_self\(self);
    elsif rising_edge(clk) then
        if enable then
            --convert slv to normal types
            var_in0 := Sfix(in0, 0, -17);

            --call the main entry
            DCRemoval_0.\_pyha_init_self\(self);
            DCRemoval_0.main(self, var_in0, ret_0=>var_out0);
            DCRemoval_0.\_pyha_update_self\(self);

            --convert normal types to slv
            out0 <= to_slv(var_out0);
        end if;
      end if;

    end process;
end architecture;