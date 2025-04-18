<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Robot Control with Speed</title>
  <style>
    button {
      padding: 15px;
      font-size: 18px;
      margin: 10px;
    }
    select {
      font-size: 16px;
      padding: 5px;
    }
  </style>
</head>
<body>
  <h1>Control the Robot</h1>
  <form method="POST">
    <label for="speed">Speed:</label>
    <select name="speed" id="speed">
      {% for s in range(0, 101, 10) %}
        <option value="{{ s }}" {% if s == speed %}selected{% endif %}>{{ s }}%</option>
      {% endfor %}
    </select>

    <div><button name="action" value="forward">⬆️ Forward</button></div>
    <div>
      <button name="action" value="left">⬅️ Left</button>
      <button name="action" value="stop">⏹️ Stop</button>
      <button name="action" value="right">➡️ Right</button>
    </div>
    <div><button name="action" value="backward">⬇️ Backward</button></div>
  </form>
</body>
</html>