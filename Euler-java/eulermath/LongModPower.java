package eulermath;

public class LongModPower {
	long[] squares;
	public LongModPower() {
	    squares = new long[64];
	}
	public long raise(long numb, long exponent, long modv) {
		squares[0] = 1;
		squares[1] = numb;
		int i = 0;
		long count = 2L;
		for (i=2; i<64; i++) {
			squares[i] = squares[i-1]*squares[i-1];
			if (modv > 0) {
				squares[i] %= modv;
			}
			if (count > exponent) {
			    break;
			}
			count *= 2L;
		}
		long product = 1L;
		long nexponent = exponent;
		count /= 2L;
		i--;
		while (nexponent > 0L) {
			if (nexponent >= count) {
				nexponent -= count;
				product *= squares[i];
				if (modv > 0) {
				    product %= modv;
				}
			}
			if (nexponent == 0) {
				return product;
			}
			count /= 2L;
			i--;
		}
	    return product;
	}
}
