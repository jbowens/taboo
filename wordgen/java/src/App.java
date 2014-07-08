import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;

import org.json.simple.JSONObject;


public class App {

	public static final int NUM_SAMPLES = 100;

	public App(String linksFile) {
		try {
			System.out.println("Creating sampler");
			WordFreqSampler sampler = new WordFreqSampler(NUM_SAMPLES, linksFile);
			sampler.genWordFreqs();
			System.out.println("Finished creating sampler");
			HashMap<String, Integer> totalUniFreqs = sampler.getTotalUniFreqs();
			HashMap<String, Integer> totalBiFreqs = sampler.getTotalBiFreqs();
			PageParser pp = new PageParser(sampler.getLinks(), totalUniFreqs, totalBiFreqs);
			JSONObject obj = pp.createWords();
			FileWriter output = new FileWriter("wiki_words_14.json");
			if (output == null) {
				System.out.println("0____0");
			}
			if (obj == null) {
				System.out.println("T__T");
			}
			output.write(obj.toJSONString());
			output.flush();
			output.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static void main(String[] args) {
		new App(args[0]);
	}

}
