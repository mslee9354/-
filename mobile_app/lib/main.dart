import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:qr_code_scanner/qr_code_scanner.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Guard Post Control',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const QRViewExample(),
    );
  }
}

class QRViewExample extends StatefulWidget {
  const QRViewExample({super.key});

  @override
  State<StatefulWidget> createState() => _QRViewExampleState();
}

class _QRViewExampleState extends State<QRViewExample> {
  final GlobalKey qrKey = GlobalKey(debugLabel: 'QR');
  Barcode? result;
  QRViewController? controller;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('QR Scan')),
      body: Column(
        children: <Widget>[
          Expanded(
            flex: 5,
            child: QRView(
              key: qrKey,
              onQRViewCreated: _onQRViewCreated,
            ),
          ),
          Expanded(
            flex: 1,
            child: Center(
              child: (result != null)
                  ? Text('Data: ${result!.code}')
                  : const Text('Scan a code'),
            ),
          )
        ],
      ),
    );
  }

  void _onQRViewCreated(QRViewController controller) {
    this.controller = controller;
    controller.scannedDataStream.listen((scanData) async {
      controller.pauseCamera();
      result = scanData;
      await _showInputDialog(scanData.code ?? '');
      controller.resumeCamera();
      setState(() {});
    });
  }

  Future<void> _showInputDialog(String qrData) async {
    final person = jsonDecode(qrData);
    final purposeController = TextEditingController();
    final destinationController = TextEditingController();
    await showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Entry Info'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: purposeController,
              decoration: const InputDecoration(labelText: '목적'),
            ),
            TextField(
              controller: destinationController,
              decoration: const InputDecoration(labelText: '행선지'),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () async {
              await _sendData(
                person,
                purposeController.text,
                destinationController.text,
              );
              Navigator.of(context).pop();
            },
            child: const Text('전송'),
          ),
        ],
      ),
    );
  }

  Future<void> _sendData(
      Map<String, dynamic> person, String purpose, String destination) async {
    final res = await http.post(
      Uri.parse('http://<SERVER_IP>:5000/check'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'person': person,
        'purpose': purpose,
        'destination': destination,
      }),
    );
    if (res.statusCode == 200) {
      final data = jsonDecode(res.body);
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text('결과: ${data['result']}')));
    } else {
      ScaffoldMessenger.of(context)
          .showSnackBar(const SnackBar(content: Text('오류')));
    }
  }
}
