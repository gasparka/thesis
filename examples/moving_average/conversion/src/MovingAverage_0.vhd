-- generated by pyha 0.0.4 at 2017-04-01 12:11:21
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

-- Moving average algorithm.
-- :param window_len: Size of the moving average window, must be power of 2
package MovingAverage_0 is

    type sfixed0_17_list_t is array (natural range <>) of sfixed(0 downto -17);

    type next_t is record
        shift_register: sfixed0_17_list_t(0 to 3);
        sum: sfixed(2 downto -17);
        \out\: sfixed(0 downto -17);
    end record;

    type self_t is record
        -- constants
        window_len: integer;
        window_pow: integer;
        \_delay\: integer;

        shift_register: sfixed0_17_list_t(0 to 3);
        sum: sfixed(2 downto -17);
        \out\: sfixed(0 downto -17);
        \next\: next_t;
    end record;

    procedure \_pyha_init_self\(self: inout self_t);

    procedure \_pyha_constants_self\(self: inout self_t);

    procedure \_pyha_reset_self\(self: inout self_t);

    procedure \_pyha_update_self\(self: inout self_t);

    -- This works by keeping a history of 'window_len' elements and sum of them.
    -- Every clock last element will be subtracted and new added to the sum.
    -- Sum is then divided by the 'window_len'.
    -- More good infos: https://www.dsprelated.com/showarticle/58.php
    -- :param x: input to average
    -- :return: averaged output
    -- :rtype: Sfix
    procedure main(self:inout self_t; x: sfixed(0 downto -17); ret_0:out sfixed(0 downto -17));
end package;

package body MovingAverage_0 is
    procedure \_pyha_init_self\(self: inout self_t) is
    begin
        self.\next\.shift_register := self.shift_register;
        self.\next\.sum := self.sum;
        self.\next\.\out\ := self.\out\;
        \_pyha_constants_self\(self);
    end procedure;

    procedure \_pyha_constants_self\(self: inout self_t) is
    begin
        self.window_len := 4;
        self.window_pow := 2;
        self.\_delay\ := 2;

    end procedure;

    procedure \_pyha_reset_self\(self: inout self_t) is
    begin
        self.\next\.shift_register := (Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17), Sfix(0.0, 0, -17));
        self.\next\.sum := Sfix(0.0, 2, -17);
        self.\next\.\out\ := Sfix(0.0, 0, -17);
        \_pyha_update_self\(self);
    end procedure;

    procedure \_pyha_update_self\(self: inout self_t) is
    begin
        self.shift_register := self.\next\.shift_register;
        self.sum := self.\next\.sum;
        self.\out\ := self.\next\.\out\;
        \_pyha_constants_self\(self);
    end procedure;



    -- This works by keeping a history of 'window_len' elements and sum of them.
    -- Every clock last element will be subtracted and new added to the sum.
    -- Sum is then divided by the 'window_len'.
    -- More good infos: https://www.dsprelated.com/showarticle/58.php
    -- :param x: input to average
    -- :return: averaged output
    -- :rtype: Sfix
    procedure main(self:inout self_t; x: sfixed(0 downto -17); ret_0:out sfixed(0 downto -17)) is

    begin

        -- add new element to shift register
        self.\next\.shift_register := x & self.shift_register(0 to self.shift_register'high-1);

        -- calculate new sum
        self.\next\.sum := resize(self.sum + x - self.shift_register(self.shift_register'length-1), 2, -17, fixed_wrap, fixed_truncate);

        -- divide sum by amount of window_len
        self.\next\.\out\ := resize(self.sum sra self.window_pow, 0, -17, fixed_wrap, fixed_truncate);
        ret_0 := self.\out\;
        return;
    end procedure;
end package body;
