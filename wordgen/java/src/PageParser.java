import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;
import java.nio.ByteBuffer;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.HashSet;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import com.google.common.collect.MinMaxPriorityQueue;

import java.util.Arrays;

public class PageParser {
	private HashSet<String> _omittedWords = new HashSet<String>(Arrays.asList(
			"her", "his", "she", "he", "the", "an", "for", "not", "a", "they", 
			"their", "us", "our", "has", "would", "such", "were", "it", "its", 
			"are", "should", "contain", "retrieved", "ext", "per", "him", "you", 
			"com", "those", "there", "had", "was", "became"));
	public static final int MAX_CHARS = 40;
	public static final String WIKI_BASE_URL = "http://en.wikipedia.org";
	private static final double ALPHA = 1.0;
	private HashMap<String, Integer> _totalUniFreqs;
	private HashMap<String, Integer> _totalBiFreqs;
	private JSONArray _links = null;
	private int _totalLinks = 0;
	
	public PageParser(JSONArray links, HashMap<String, Integer> totalUniFreqs, 
			HashMap<String, Integer> totalBiFreqs) {
		_totalUniFreqs = totalUniFreqs;
		_totalBiFreqs = totalBiFreqs;
		_links = links;
		_totalLinks = _links.size();
	}
	
	public JSONObject createWords() throws IOException {
		JSONObject obj = new JSONObject();
		for (int i=3500; i<3900; i++) {
			Object ele = _links.get(i);
			String link = (String)ele;
			String content = getUrlSource(WIKI_BASE_URL+link);
			// TODO also consider getting rid of notes section
			int refIdx = content.indexOf("<h2><span class=\"mw-headline\" id=\"References\">References</span></h2>");
			refIdx = (refIdx >= 0) ? refIdx : content.length();
			int sourceIdx = content.indexOf("<h2><span class=\"mw-headline\" id=\"Citations\">Citations</span></h2>");
			sourceIdx = (sourceIdx >= 0) ? sourceIdx : content.length();
			String cutContent = content.substring(0, Math.min(refIdx, sourceIdx));
			String MLlessContent = cutContent.replaceAll("\\<.*?>"," ");
//			String MLlessContent = Jsoup.parse(content).text();
			int endIdx = MLlessContent.indexOf("- Wikipedia");
			if (endIdx != -1 && endIdx <= MAX_CHARS) {
				String pageName = MLlessContent.substring(0, endIdx).trim();
				System.out.println(i + ": Handling wiki page " + pageName);
				try {
					int nameNum =Integer.parseInt(pageName.replaceAll("[\\D]", ""));
					if (nameNum > 1000 && nameNum <= 2013) {
						continue;
					}
				} catch (NumberFormatException e) {
					// nothing
				}
				if (pageName.length() > 7) {
					if (pageName.substring(0, 7).equals("List of")) {
						continue;
					}
				}
				JSONArray arr = extractProhibitedFromContent(pageName, MLlessContent);
				obj.put(pageName, arr);
			}
		}
		return obj;
	}
	
	public JSONArray extractProhibitedFromContent(String pageName, String content) throws IOException {
		JSONArray arr = new JSONArray();
		HashMap<String, Integer> docUniFreqs = new HashMap<String, Integer>();
		HashMap<String, Integer> docBiFreqs = new HashMap<String, Integer>();
		String strippedContent = WordFreqSampler.stripPunc(content);
		String[] words = strippedContent.split(" ");
		if (words.length > 0) {
			docUniFreqs.put(words[0], 1);
		}
		for (int j=1; j<words.length; j++) {
			String currBigram = words[j] + " " + words[j-1];
			int uniCount = (docUniFreqs.get(words[j]) != null) ? 
					docUniFreqs.get(words[j]) : 0;
			int biCount = (docBiFreqs.get(currBigram) != null) ? 
					docBiFreqs.get(currBigram) : 0;
			docUniFreqs.put(words[j], uniCount+1);
			docBiFreqs.put(currBigram, biCount+1);
		}
		int totalUniInDoc = 0;
		int totalBiInDoc = 0;
		for (Integer value : docUniFreqs.values()) {
			totalUniInDoc += value;
		}
		for (Integer value : docBiFreqs.values()) {
			totalBiInDoc += value;
		}
		MinMaxPriorityQueue<NGramValuePair> q = 
				getUniLikelihoods(null, docUniFreqs, totalUniInDoc, 15);
//			q = getBiLikelihoods(q, docBiFreqs, totalBiInDoc, 15);
		while (!q.isEmpty()) {
			NGramValuePair p = q.pollFirst();
			if (p._word.length() < 3) {
				continue;
			}
			Character lastChar = p._word.charAt(p._word.length()-1);
			String cleanWord = p._word;
			if (lastChar == 's' || lastChar == 'n') {
				cleanWord = cleanWord.substring(0, cleanWord.length()-1);
			}
			if (p._word.substring(p._word.length()-2, p._word.length()-1) == "es") {
				cleanWord = cleanWord.substring(0, cleanWord.length()-1);
			}
			if (pageName.toLowerCase().indexOf(cleanWord) < 0 && 
					!_omittedWords.contains(p._word)) {
				arr.add(p._word);
			}
		}
		return arr;
	}
	
	public MinMaxPriorityQueue<NGramValuePair> getUniLikelihoods(
			MinMaxPriorityQueue<NGramValuePair> queue, 
			HashMap<String, Integer> unigramFreqs, 
			int totalUniInDoc, int maxSize) {
		MinMaxPriorityQueue<NGramValuePair> q = 
				(MinMaxPriorityQueue<NGramValuePair>) 
				((queue == null) ? MinMaxPriorityQueue.create() : queue);
		for (String word : unigramFreqs.keySet()) {
			try {
				if (Integer.valueOf(word) > 1000 && Integer.valueOf(word) < 2013) {
					continue;
				}
			} catch (NumberFormatException e) {
				// nothing
			}
			int total_count = (_totalUniFreqs.get(word) != null) ? 
					_totalUniFreqs.get(word)*_totalLinks : 0;
			double numerator = (double)unigramFreqs.get(word)+ALPHA;
			double denom = (double)total_count+(ALPHA*_totalUniFreqs.size());
			double r = numerator/denom;
			q.add(new NGramValuePair(word, r));
			if (q.size() > maxSize) {
				q.removeLast();
			}
		}
		return q;
	}
	
	public MinMaxPriorityQueue<NGramValuePair> getBiLikelihoods(
			MinMaxPriorityQueue<NGramValuePair> queue, 
			HashMap<String, Integer> bigramFreqs, 
			int totalBiInDoc, 
			int maxSize) {
		MinMaxPriorityQueue<NGramValuePair> q = 
				(MinMaxPriorityQueue<NGramValuePair>) 
				((queue == null) ? MinMaxPriorityQueue.create() : queue);
		for (String word : bigramFreqs.keySet()) {
			
			try {
				if (Integer.valueOf(word) > 1000 && Integer.valueOf(word) < 2013) {
					continue;
				}
			} catch (NumberFormatException e) {
				// nothing
			}
			
			int total_count = (_totalBiFreqs.get(word) != null) ? 
					_totalBiFreqs.get(word)*_totalLinks : 0;
			double numerator = (double)bigramFreqs.get(word)+ALPHA;
			double denom = (double)total_count+(ALPHA*_totalBiFreqs.size());
			double r = numerator/denom;
			q.add(new NGramValuePair(word, r));
			if (q.size() > maxSize) {
				q.removeLast();
			}
		}
		return q;
	}
	
	private class NGramValuePair implements Comparable {

		private String _word;
		public double _value;
		
		public NGramValuePair(String word, double value) {
			_word = word;
			_value = value;
		}
		
		@Override
		public int compareTo(Object o) {
			if (this._value < ((NGramValuePair)o)._value) {
				return 1;
			} else if (this._value > ((NGramValuePair)o)._value) {
				return -1;
			} else {
				return 0;
			}
		}
	}
	
	public static String getUrlSource(String link) throws IOException {
        URL url = new URL(link);
        URLConnection c = url.openConnection();
        BufferedReader in = new BufferedReader(new InputStreamReader(
                c.getInputStream(), "UTF-8"));
        String inputLine;
        StringBuilder a = new StringBuilder();
        while ((inputLine = in.readLine()) != null)
            a.append(inputLine);
        in.close();
        return a.toString();
    }
}
