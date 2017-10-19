package eulermath;

public class Sieve {
	private final static int[] pindex = new int[]
			{1, 7, 11, 13, 17, 19, 23, 29};
	private final static int sievesz = 9000000;
	private final static int tblsize = (sievesz/30) * 8;
	private boolean table[];
	private int divlist[];
    private int start_pt;
    private int tbl_indx;
    private int prm_indx;
	private int out_buffer[];
	private int obuf_ind;
	private int nb_index;
	private int maxprime;
	public Sieve(int size) {
	    divlist = new int[(size > 100000000) ? 10000 : 2000];
	    table = new boolean[tblsize];
	    table[0] = true;
	    start_pt = 0;
	    tbl_indx = 1;
	    prm_indx = 0;
	    maxprime = size;
	    do_first_sieve();
	    out_buffer = new int[10];
	    obuf_ind = 3;
	    out_buffer[0] = 2;
	    out_buffer[1] = 3;
	    out_buffer[2] = 5;
	    tbl_indx = 1;
	    nb_index = 10;
	}
	private void do_first_sieve() {
		while (tbl_indx < tblsize) {
			if (! table[tbl_indx]) {
				// System.out.println(unconv(tbl_indx));
			    int nval = unconv(tbl_indx);
			    int strt_srch = nval * nval;
			    if (strt_srch >= sievesz) {
			    	break;
			    }
			    divlist[prm_indx] = nval;
			    prm_indx++;
			    while (strt_srch < sievesz) {
			    	int tindx = conv(strt_srch);
			    	if (tindx > 0) {
			    	    table[tindx] = true;
			    	}
			    	strt_srch += 2 * nval;
			    }
			}
			tbl_indx++;
		}
		int pnum = divlist[prm_indx-1];
		int stp = conv(pnum) + 1;
		while (pnum * pnum < maxprime) {
			while (table[stp]) {
				stp++;
			}
			pnum = unconv(stp);
			divlist[prm_indx] = pnum;
			prm_indx++;
			stp++;
		}
		divlist[prm_indx] = 0;
		return;
	}
	private void do_later_sieve() {
		for (int i=0; i<tblsize; i++) {
			table[i] = false;
		}
		for (int i=0; i<divlist.length; i++) {
			if (divlist[i] == 0) {
				break;
			}
			int sp = divlist[i] - (start_pt % divlist[i]);
			int spconv = conv(sp);
			while (spconv == -1) {
				sp += divlist[i];
				spconv = conv(sp);
			}
			int step = divlist[i] * 2;
			while (sp < sievesz) {
			    spconv = conv(sp);
			    if (spconv != -1) {
			    	table[spconv] = true;
			    }
			    sp += step;
			}
		}
		obuf_ind = 0;
		nb_index = 0;
		tbl_indx = 0;
	}
	private final static int conv(int number) {
		int row = number / 30; 
		int indx = number % 30;
		int col;
		for (col=0; col<pindex.length;  col++) {
            if (pindex[col] == indx) {
                break;
            }
		}
		if (col == pindex.length) {
			return -1;
		}
		return row*8 + col;
	}
	private final static int unconv(int number) {
		int row = number / 8;
	    int col = pindex[number % 8];
	    return row * 30 + col;
	}
	public void get_next_block() {
		while (obuf_ind < 10) {
			if (tbl_indx >= tblsize) {
				break;
			}
			while (table[tbl_indx]) {
				tbl_indx++;
				if (tbl_indx >= tblsize) {
					out_buffer[obuf_ind] = 0;
					nb_index = 0;
					return;
				}
			}
			out_buffer[obuf_ind] = unconv(tbl_indx) + start_pt;
			tbl_indx++;
			obuf_ind++;
			if (tbl_indx >= tblsize) {
				if (obuf_ind < 10) {
				    out_buffer[obuf_ind] = 0;
				    nb_index = 0;
				    return;
				}
			}
		}
		obuf_ind = 0;
		nb_index = 0;
		return;
	}
	
	public int get_next() {
		if (nb_index >= 10) {
			get_next_block();
		}
		int retv = out_buffer[nb_index];
		nb_index++;
		if (retv > maxprime) {
			return 0;
		}
		if (retv == 0) {
		    start_pt += sievesz;
		    if (start_pt < maxprime) {
		    	do_later_sieve();
		    	get_next_block();
		    	//for (int ii=0; ii < 10; ii++) System.out.println(out_buffer[ii]);
		    	retv = out_buffer[nb_index];
		    	nb_index++;
		    }
		}
		return retv;
	}
	public static void main(String[] args) {
	    eulermath.Sieve sv = new eulermath.Sieve(100000000);
	    int x = -1;
	    while (x != 0) {
	    	int prev = x;
	    	x = sv.get_next();
	    	if (x == prev) System.out.println(x);
	    	if (x == 9000011) System.out.println(x);
	    }
	}
}
