import java.io.IOException;
import java.util.HashMap;


public class App {

	public static final int NUM_SAMPLES = 50;
	
	public App(String linksFile) {
		try {
			WordFreqSampler sampler = new WordFreqSampler(NUM_SAMPLES, linksFile);
			HashMap<String, Integer> totalWordFreqs = sampler.getWordFreqs();
			PageParser pp = new PageParser(linksFile, totalWordFreqs);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		new App(args[0]);
	}
	
}
