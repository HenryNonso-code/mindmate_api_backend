import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load(fileName: ".env");
  runApp(const MindMateApp());
}

class MindMateApp extends StatefulWidget {
  const MindMateApp({super.key});

  @override
  State<MindMateApp> createState() => _MindMateAppState();
}

class _MindMateAppState extends State<MindMateApp> {
  bool _isDarkMode = false;

  @override
  void initState() {
    super.initState();
    _loadTheme();
  }

  Future<void> _loadTheme() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() => _isDarkMode = prefs.getBool("darkMode") ?? false);
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MindMate AI',
      themeMode: _isDarkMode ? ThemeMode.dark : ThemeMode.light,
      theme: ThemeData.light(),
      darkTheme: ThemeData.dark(),
      debugShowCheckedModeBanner: false,
      home: HomeScreen(
        isDarkMode: _isDarkMode,
        onToggleTheme: (val) async {
          final prefs = await SharedPreferences.getInstance();
          await prefs.setBool("darkMode", val);
          setState(() => _isDarkMode = val);
        },
      ),
    );
  }
}

class HomeScreen extends StatefulWidget {
  final bool isDarkMode;
  final Function(bool) onToggleTheme;

  const HomeScreen({super.key, required this.isDarkMode, required this.onToggleTheme});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _moodController = TextEditingController();
  String? _affirmation;
  bool _loading = false;
  List<String> _history = [];

  @override
  void initState() {
    super.initState();
    _loadHistory();
  }

  Future<void> _loadHistory() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() => _history = prefs.getStringList('affirmations') ?? []);
  }

  Future<void> fetchAffirmation() async {
    final mood = _moodController.text.trim();
    if (mood.isEmpty) return;

    setState(() {
      _loading = true;
      _affirmation = null;
    });

    final apiUrl = dotenv.env['API_URL'];
    final url = '$apiUrl/affirmation?mood=$mood';

    try {
      final response = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 10));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final affirmation = data['affirmation'];

        setState(() {
          _affirmation = affirmation;
        });

        final prefs = await SharedPreferences.getInstance();
        final history = prefs.getStringList('affirmations') ?? [];
        history.add("Mood: $mood → $affirmation");
        await prefs.setStringList('affirmations', history);
        setState(() => _history = history);
      } else {
        setState(() => _affirmation = "Error: Could not fetch affirmation.");
      }
    } catch (e) {
      setState(() => _affirmation = "Connection error: $e");
    } finally {
      setState(() => _loading = false);
    }
  }

  Future<void> _clearHistory() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('affirmations');
    setState(() => _history = []);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("MindMate AI"),
        centerTitle: true,
        actions: [
          IconButton(
            icon: Icon(widget.isDarkMode ? Icons.dark_mode : Icons.light_mode),
            onPressed: () => widget.onToggleTheme(!widget.isDarkMode),
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            const Text("How are you feeling?", style: TextStyle(fontSize: 18)),
            const SizedBox(height: 10),
            TextField(
              controller: _moodController,
              decoration: const InputDecoration(
                hintText: "Enter your mood (e.g., anxious, happy)...",
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _loading ? null : fetchAffirmation,
              child: _loading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text("Get Affirmation"),
            ),
            const SizedBox(height: 20),
            if (_affirmation != null)
              Text(
                _affirmation!,
                textAlign: TextAlign.center,
                style: const TextStyle(fontSize: 20, fontStyle: FontStyle.italic),
              ),
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text("Past Affirmations", style: TextStyle(fontWeight: FontWeight.bold)),
                TextButton(
                  onPressed: _clearHistory,
                  child: const Text("Clear", style: TextStyle(color: Colors.red)),
                ),
              ],
            ),
            Expanded(
              child: _history.isEmpty
                  ? const Text("No affirmations yet.")
                  : ListView.builder(
                      itemCount: _history.length,
                      itemBuilder: (context, index) => ListTile(
                        title: Text(_history[index]),
                      ),
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
