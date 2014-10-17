module top (out,a,b,c,d,e,f);
output out;
input a;
input b;
input c;
input d;
wire e;
wire f;
and (e,a,b);
or (f,c,d);
xor(out,e,f);
endmodule