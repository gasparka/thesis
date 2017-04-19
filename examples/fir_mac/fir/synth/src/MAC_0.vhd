-- generated by pyha 0.0.4 at 2017-04-18 19:49:59
library ieee;
    use ieee.std_logic_1164.all;
    use ieee.numeric_std.all;
    use ieee.fixed_float_types.all;
    use ieee.fixed_pkg.all;
    use ieee.math_real.all;

library work;
    use work.ComplexTypes.all;
    use work.PyhaUtil.all;
    use work.all;


package MAC_0 is



    type next_t is record
        coef: sfixed(0 downto -17);
        acc: sfixed(1 downto -34);
    end record;

    type self_t is record
        -- constants
        \_delay\: integer;

        coef: sfixed(0 downto -17);
        acc: sfixed(1 downto -34);
        \next\: next_t;
    end record;

    procedure \_pyha_init_self\(self: inout self_t);

    procedure \_pyha_constants_self\(self: inout self_t);

    procedure \_pyha_reset_self\(self: inout self_t);

    procedure \_pyha_update_self\(self: inout self_t);


    procedure main(self:inout self_t; a: sfixed(0 downto -17); sum_in: sfixed(1 downto -34); ret_0:out sfixed(1 downto -34));
end package;

package body MAC_0 is
    procedure \_pyha_init_self\(self: inout self_t) is
    begin
        self.\next\.coef := self.coef;
        self.\next\.acc := self.acc;
        \_pyha_constants_self\(self);
    end procedure;

    procedure \_pyha_constants_self\(self: inout self_t) is
    begin
        self.\_delay\ := 1;

    end procedure;

    procedure \_pyha_reset_self\(self: inout self_t) is
    begin
        self.\next\.coef := Sfix(0.36710735883668366, 0, -17);
        self.\next\.acc := Sfix(0.0, 1, -34);
        \_pyha_update_self\(self);
    end procedure;

    procedure \_pyha_update_self\(self: inout self_t) is
    begin
        self.coef := self.\next\.coef;
        self.acc := self.\next\.acc;
        \_pyha_constants_self\(self);
    end procedure;


    procedure main(self:inout self_t; a: sfixed(0 downto -17); sum_in: sfixed(1 downto -34); ret_0:out sfixed(1 downto -34)) is
        variable mul: sfixed(1 downto -34);
    begin
        mul := self.coef * a;
        self.\next\.acc := resize(mul + sum_in, 1, -34, fixed_wrap, fixed_truncate);
        ret_0 := self.acc;
        return;
    end procedure;
end package body;
