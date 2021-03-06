-- generated by pyha 0.0.4 at 2017-04-01 22:23:31
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

-- Based on: https://www.dsprelated.com/showarticle/58.php
package DCRemoval_0 is

    type MovingAverage_0_list_t is array (natural range <>) of MovingAverage_0.self_t;
    type sfixed0_17_list_t is array (natural range <>) of sfixed(0 downto -17);

    type next_t is record
        mavg: MovingAverage_0_list_t(0 to 3);
        group_delay: integer;
        input_shr: sfixed0_17_list_t(0 to 69);
        \out\: sfixed(0 downto -17);
    end record;

    type self_t is record
        -- constants
        \_delay\: integer;

        mavg: MovingAverage_0_list_t(0 to 3);
        group_delay: integer;
        input_shr: sfixed0_17_list_t(0 to 69);
        \out\: sfixed(0 downto -17);
        \next\: next_t;
    end record;

    procedure \_pyha_init_self\(self: inout self_t);

    procedure \_pyha_constants_self\(self: inout self_t);

    procedure \_pyha_reset_self\(self: inout self_t);

    procedure \_pyha_update_self\(self: inout self_t);


    procedure main(self:inout self_t; x: sfixed(0 downto -17); ret_0:out sfixed(0 downto -17));
end package;

package body DCRemoval_0 is
    procedure \_pyha_init_self\(self: inout self_t) is
    begin
        MovingAverage_0.\_pyha_init_self\(self.mavg(0));
        MovingAverage_0.\_pyha_init_self\(self.mavg(1));
        MovingAverage_0.\_pyha_init_self\(self.mavg(2));
        MovingAverage_0.\_pyha_init_self\(self.mavg(3));
        self.\next\.group_delay := self.group_delay;
        self.\next\.input_shr := self.input_shr;
        self.\next\.\out\ := self.\out\;
        \_pyha_constants_self\(self);
    end procedure;

    procedure \_pyha_constants_self\(self: inout self_t) is
    begin
        self.\_delay\ := 71;
        MovingAverage_0.\_pyha_constants_self\(self.mavg(0));
        MovingAverage_0.\_pyha_constants_self\(self.mavg(1));
        MovingAverage_0.\_pyha_constants_self\(self.mavg(2));
        MovingAverage_0.\_pyha_constants_self\(self.mavg(3));
    end procedure;

    procedure \_pyha_reset_self\(self: inout self_t) is
    begin
        self.mavg(0).\next\.shift_register := (Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17));
        self.mavg(0).\next\.sum := Sfix(0.0, 5, -17);
        self.mavg(0).\next\.\out\ := Sfix(0.0, 0, -17);
        self.mavg(1).\next\.shift_register := (Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17));
        self.mavg(1).\next\.sum := Sfix(0.0, 5, -17);
        self.mavg(1).\next\.\out\ := Sfix(0.0, 0, -17);
        self.mavg(2).\next\.shift_register := (Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17));
        self.mavg(2).\next\.sum := Sfix(0.0, 5, -17);
        self.mavg(2).\next\.\out\ := Sfix(0.0, 0, -17);
        self.mavg(3).\next\.shift_register := (Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17));
        self.mavg(3).\next\.sum := Sfix(0.0, 5, -17);
        self.mavg(3).\next\.\out\ := Sfix(0.0, 0, -17);
        self.\next\.group_delay := 62;
        self.\next\.input_shr := (Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17));
        self.\next\.\out\ := Sfix(0.0, 0, -17);
        \_pyha_update_self\(self);
    end procedure;

    procedure \_pyha_update_self\(self: inout self_t) is
    begin
        MovingAverage_0.\_pyha_update_self\(self.mavg(0));
        MovingAverage_0.\_pyha_update_self\(self.mavg(1));
        MovingAverage_0.\_pyha_update_self\(self.mavg(2));
        MovingAverage_0.\_pyha_update_self\(self.mavg(3));
        self.group_delay := self.\next\.group_delay;
        self.input_shr := self.\next\.input_shr;
        self.\out\ := self.\next\.\out\;
        \_pyha_constants_self\(self);
    end procedure;




    procedure main(self:inout self_t; x: sfixed(0 downto -17); ret_0:out sfixed(0 downto -17)) is
        variable tmp: sfixed(0 downto -17);
    begin
        -- run signal over all moving averagers
        tmp := x;
        for \_i_\ in self.mavg'range loop
            MovingAverage_0.main(self.mavg(\_i_\), tmp, ret_0=>tmp);

        end loop;
        -- subtract from delayed input
        self.\next\.input_shr := x & self.input_shr(0 to self.input_shr'high-1);
        self.\next\.\out\ := resize(self.input_shr(self.input_shr'length-1) - tmp, 0, -17, fixed_saturate, fixed_round);
        ret_0 := self.\out\;
        return;
    end procedure;
end package body;
