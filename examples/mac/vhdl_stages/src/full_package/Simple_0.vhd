package Simple_0 is
    type next_t is record
        coef: integer;
        mul: integer;
        acc: integer;
    end record;

    type self_t is record
        coef: integer;
        mul: integer;
        acc: integer;
		  
        nexts: next_t;
    end record;

    procedure reset(self: inout self_t);
    procedure update_registers(self: inout self_t);
    procedure main(self:inout self_t; a: integer; ret_0:out integer);
end package;

package body Simple_0 is

    procedure reset(self: inout self_t) is
    begin
        self.nexts.coef := 123;
        self.nexts.mul := 0;
        self.nexts.acc := 0;
        update_registers(self);
    end procedure;

    procedure update_registers(self: inout self_t) is
    begin
        self.coef := self.nexts.coef;
        self.mul := self.nexts.mul;
        self.acc := self.nexts.acc;
    end procedure;

    procedure main(self:inout self_t; a: integer; ret_0:out integer) is
    begin
        self.nexts.mul := self.coef * a;
        self.nexts.acc := self.acc + self.mul;
        ret_0 := self.acc;
        return;
    end procedure;
end package body;
