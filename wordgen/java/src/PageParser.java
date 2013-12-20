import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;

import org.json.simple.JSONArray;
import org.json.simple.JSONValue;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class PageParser {
	
	public static final int MAX_CHARS = 40;
	public static final String WIKI_BASE_URL = "http://en.wikipedia.org";
	private HashMap<String, Integer> _totalWordFreqs;
	
	public PageParser(String linksFile, HashMap<String, Integer> totalWordFreqs) throws IOException {
		_totalWordFreqs = totalWordFreqs;
		String link_data = readFile(linksFile, StandardCharsets.UTF_8);
		Object jsonObj = JSONValue.parse(link_data);
		JSONArray arr = (JSONArray)jsonObj;
		for (Object ele : arr) {
			String link = (String)ele;
			handleWikiURL(link);
		}
	}
	
	public void handleWikiURL(String link) throws IOException {
		Document doc = Jsoup.connect(WIKI_BASE_URL+link).get();
		String content = doc.text();
		int endIdx = content.indexOf("- Wikipedia");
		if (endIdx != -1 && endIdx <= MAX_CHARS) {
			String name = content.substring(0, endIdx);
			HashMap<String, Integer> unigramFreqs = getUnigramFreqs(content);
			HashMap<String, Integer> bigramFreqs = getBigramFreqs(content);
		}
		
	// TODO filter out names with years in them
	// TODO use unigrams and bigrams to get prohibited terms
	}
	
	public HashMap<String, Integer> getUnigramFreqs(String content) {
		return null;
	}
	
	public HashMap<String, Integer> getBigramFreqs(String content) {
		return null;
	}
	
	public void getUnigramLikihoods(HashMap<String, Integer> unigramFreqs) {
		
	}
	
	static String readFile(String path, Charset encoding) 
			throws IOException {
			  byte[] encoded = Files.readAllBytes(Paths.get(path));
			  return encoding.decode(ByteBuffer.wrap(encoded)).toString();
			}
	
}
