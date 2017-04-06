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