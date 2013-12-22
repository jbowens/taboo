import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Random;
import java.net.URL;
import java.net.URLConnection;

import org.json.simple.JSONArray;
import org.json.simple.JSONValue;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

/**
 * 
 * @author florajin
 *
 */


public class WordFreqSampler {

	
	private int _numSamples;
	private JSONArray _links = null;
	private HashMap<String, Integer> _totalUniFreqs;
	private HashMap<String, Integer> _totalBiFreqs;
	
	public WordFreqSampler(Integer numSamples, String linksFile) throws IOException {
		_totalUniFreqs = null;
		_totalBiFreqs = null;
		_numSamples = numSamples;
		String link_data = readFile(linksFile, StandardCharsets.UTF_8);
		Object jsonObj = JSONValue.parse(link_data);
		_links = (JSONArray)jsonObj;
	}
	
	public JSONArray getLinks() {
		return _links;
	}
	
	public void genWordFreqs() throws IOException {
		Random rng = new Random();
		int maxRange = _links.size();
		HashSet<Integer> idxSet = new HashSet<Integer>();
		// Generate random samples
		while (idxSet.size() < _numSamples) {
			Integer toAdd = rng.nextInt(maxRange);
			idxSet.add(toAdd);
		}
		HashMap<String, Integer> uniFreqs = new HashMap<String, Integer>();
		HashMap<String, Integer> biFreqs = new HashMap<String, Integer>();
		
		for (int i=0; i<_numSamples; i++) {
			System.out.println("Doc #" + (i+1));
			String link = (String)_links.get(i);
//			Document doc = Jsoup.connect(PageParser.WIKI_BASE_URL+link).get();
//			String content = stripPunc(doc.text());
			String content = PageParser.getUrlSource(PageParser.WIKI_BASE_URL+link);
			int refIdx = content.indexOf("<h2><span class=\"mw-headline\" id=\"References\">References</span></h2>");
			refIdx = (refIdx >= 0) ? refIdx : content.length();
			int sourceIdx = content.indexOf("<h2><span class=\"mw-headline\" id=\"Citations\">Citations</span></h2>");
			sourceIdx = (sourceIdx >= 0) ? sourceIdx : content.length();
			String cutContent = content.substring(0, Math.min(refIdx, sourceIdx));
			String MLlessContent = stripPunc(cutContent.replaceAll("\\<.*?>"," "));
			String[] words = MLlessContent.split(" ");
			if (words.length > 0) {
				uniFreqs.put(words[0], 1);
			}
			for (int j=1; j<words.length; j++) {
				String currBigram = words[j] + " " + words[j-1];
				int uniCount = (uniFreqs.get(words[j]) != null) ? uniFreqs.get(words[j]) : 0;
				int biCount = (biFreqs.get(currBigram) != null) ? biFreqs.get(currBigram) : 0;
				uniFreqs.put(words[j], uniCount+1);
				biFreqs.put(currBigram, biCount+1);
			}
		}
		for (String key : uniFreqs.keySet()) {
			uniFreqs.put(key, uniFreqs.get(key)/_numSamples);
		}
		for (String key : biFreqs.keySet()) {
			biFreqs.put(key, biFreqs.get(key)/_numSamples);
		}
		
		_totalUniFreqs = uniFreqs;
		_totalBiFreqs = biFreqs;
	}
	
	public static String stripPunc(String input){
	    final StringBuilder strBuilder = new StringBuilder();
	    for(final char c : input.toCharArray())
	        if (Character.isLetter(c)) {
	        	strBuilder.append(Character.isLowerCase(c) ? c : Character.toLowerCase(c));
	        } else {
	        	strBuilder.append(" ");
	        }
	    return strBuilder.toString();
	}
	
	public HashMap<String, Integer> getTotalUniFreqs() {
		return _totalUniFreqs;
	}
	
	public HashMap<String, Integer> getTotalBiFreqs() {
		return _totalBiFreqs;
	}
	
	static String readFile(String path, Charset encoding) 
			throws IOException {
		byte[] encoded = Files.readAllBytes(Paths.get(path));
		return encoding.decode(ByteBuffer.wrap(encoded)).toString();
	}
	
}
