from dotenv import load_dotenv
load_dotenv()

import os

title = os.getenv('TITLE')
background_image_path = os.getenv('BACKGROUND_IMAGE_PATH')

# Flutterサンプルコード

# import 'dart:convert';
# import 'package:http/http.dart' as http;

# Future<void> postImageUrl() async {
#   const String apiUrl = 'http://192.168.11.32:5000/display';

#   final Map<String, dynamic> data = {
#     "url": 画像のURL
#   };

#   try {
#     final response = await http.post(
#       Uri.parse(apiUrl),
#       headers: {
#         "Content-Type": "application/json",
#       },
#       body: jsonEncode(data),
#     );

#     if (response.statusCode == 200) {
#       print("Success: ${response.body}");
#     } else {
#       print("Failed with status: ${response.statusCode}");
#       print("Body: ${response.body}");
#     }
#   } catch (e) {
#     print("Error: $e");
#   }
# }
