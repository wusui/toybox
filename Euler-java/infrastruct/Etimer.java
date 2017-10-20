package infrastruct;

public class Etimer {
	private static long nanodiv = 1000000000L;
	public static void run_function(EulerProb prob) {
    	long timev = System.nanoTime();
    	String answer = prob.problem();
    	System.out.println(answer);
    	long exectime = System.nanoTime() - timev;
    	long secs = exectime / nanodiv;
    	long nanosecs = exectime % nanodiv;
    	long millisecs = (nanosecs + 500000L) / 1000000L;
    	System.out.println(String.format("%d.%03d", secs, millisecs));
	}
}
