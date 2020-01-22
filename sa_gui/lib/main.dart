import 'dart:io';
import 'dart:ui';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:url_launcher/url_launcher.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Foo Sentiment Analysis Runner',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'Foo Sentiment Analysis Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);
  final String title;
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String getSentiment(num score) {
    // order of these is important
    if (score < -0.75) 
      return 'Very Negative';
    if (score < -0.25)
      return 'Negative';
    if (score > 0.75)
      return 'Very Positive';
    if (score > 0.25)
      return 'Positive';
    if (score >= -.25 && score <= 0.25)
      return 'Neutral';
    else
      return 'Unclear Sentiment: '+score.toStringAsFixed(4);
  }

  _launchURL() async {
    const url = 'https://google.com.br';
    if (await canLaunch(url)) {
      await launch(url);
    } else {
      throw 'Could not launch $url';
    }
  }

  void _showHelp() {
    print('showHelp clicked');
    setState(() {
//      _counter++;
    });
  }

  void _submit() async {
    print('submit clicked');
    print(colorList);
    // need to swap out hostname
    //   var host = '10.0.2.2:5000';   // for android emulator
    //   var host = '127.0.0.1:5000';   // for web testing
    var host = 'flaskmli.azurewebsites.net';   // prod host
    var response = await http.get('http://'+host+'/nlp/sa/all?data='+inputController.text);
    print('Response status: ${response.statusCode}');
    print('Response body: ${response.body}');
    print(inputController.text);

    var resp = response.body;
    Map<String, dynamic> nlps = jsonDecode(resp);
    List<dynamic> results = nlps['results'];

    List<Map<String, dynamic>> dataList = [];

    results.forEach((result) {
      dataList.add(result);
    });

    colorList.add(Colors.green[50]);

    Container container = buildContainer(dataList, colorList.length-1);
    contentList.add(container);
    inputController.text = '';

    FocusScope.of(context).requestFocus(FocusNode());
    setState(() {
      for (var i=0; i<colorList.length; i++) {
        colorList[i] = Colors.grey;
      }
    });
  }

  final inputController = TextEditingController();
  final List<Widget> contentList = [];
  final List<Color> colorList = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: ListView(
        children: <Widget>[

        Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
//          crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              Padding(padding: EdgeInsets.only(top: 20.0)),
              Text('Foo Sentiment Multi Analyzer',
                style: new TextStyle(color: Colors.blue, fontSize: 25.0),),
              Padding(padding: EdgeInsets.only(top: 25.0)),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: TextFormField(
                  controller: inputController,
                  maxLines: 3,
                  onFieldSubmitted: (term) {
                    print('what is this '+ term);
                    FocusScope.of(context).requestFocus(FocusNode());
                  },
                  textInputAction: TextInputAction.done,
                  decoration: new InputDecoration(
                    labelText: "New Text to Analyze",
                    fillColor: Colors.white,
                    border: new OutlineInputBorder(
                      borderRadius: new BorderRadius.circular(25.0),
                      borderSide: new BorderSide(
                      ),
                    ),
                    //fillColor: Colors.green
                  )
                ),
              ),
               FlatButton (
                child: Text('Go'),
                color: Colors.blue,
                textColor: Colors.white,
                onPressed: _submit,
              ),
              Divider(),
              Padding(padding: EdgeInsets.only(top: 22.0)),
              Text('Results',
                style: new TextStyle(color: Colors.blue, fontSize: 15.0),),
              Wrap(
                direction: Axis.horizontal,
                children: contentList,
              )
            ],
          ),
        ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _showHelp,
        tooltip: 'Help',
        child: Icon(Icons.help),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }

  Container buildContainer(List<Map<String, dynamic>> dataList, num ind) {
    return Container(
      margin: new EdgeInsets.all(10.0),
      color: colorList[ind],
      child: Column (
        children: <Widget>[
          ConstrainedBox(
            constraints: BoxConstraints(minWidth: 250),
            child: DataTable(
              columns: [
                DataColumn(label: Text('Model', style: new TextStyle(fontWeight: FontWeight.bold, color:Colors.blue, fontSize: 12.0), )),
                DataColumn(label: Text('Score', style: new TextStyle(fontWeight: FontWeight.bold, color:Colors.blue, fontSize: 12.0),)),
                DataColumn(label: Text('Sentiment', style: new TextStyle(fontWeight: FontWeight.bold, color:Colors.blue, fontSize: 12.0),)),
              ],
              rows:
              dataList // Loops through dataColumnText, each iteration assigning the value to element
                  .map(((element) => DataRow(
                cells: <DataCell>[
                  DataCell(
                    GestureDetector(
                      child: Text(element["model"], style: TextStyle(decoration: TextDecoration.underline, color: Colors.blue)),
                      onTap: _launchURL)
                  ), //Extracting from Map element the value
                  DataCell(Text(element["nScore"].toStringAsFixed(4))),
                  DataCell(Text(getSentiment(element["nScore"]))),
                ],
              )),
              ).toList(),
            ),
          ),
          Text('Evaluated: ',  style: new TextStyle(color: Colors.orange, fontWeight: FontWeight.bold, fontSize: 15.0),),
          Text(inputController.text, style: new TextStyle(color: Colors.orange, fontStyle: FontStyle.italic, fontSize: 15.0),),
        ],
      ),
    );
  }
}
