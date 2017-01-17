package com.gm.gislain.tvshowapp;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.gm.gislain.tvshowapp.Model.User;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;


public class LoginActivity extends AppCompatActivity{

    private final String SIGN_IN_URL = "http://10.0.2.2:5000/users";

    private EditText mLoginView;
    private EditText mPasswordView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        mLoginView = (EditText) findViewById(R.id.login);
        mPasswordView = (EditText) findViewById(R.id.password);

        Button mSignInButton = (Button) findViewById(R.id.email_sign_in_button);
        mSignInButton.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view) {
                attemptLogin();
            }
        });
    }

    private void attemptLogin() {

        String login = mLoginView.getText().toString();
        String password = mPasswordView.getText().toString();

        if (TextUtils.isEmpty(login) || TextUtils.isEmpty(password)) {
            Toast.makeText(this, R.string.error_field_required, Toast.LENGTH_LONG).show();
        } else {
            connectToServeur(login, password);
        }
    }

    public void connectToServeur(String login, String password) {
        final String log = login;
        final String pass = password;

        Map<String,String> params = new HashMap<>();
        params.put(User.KEY_LOGIN,log);
        params.put(User.KEY_PASSWORD,pass);

        JsonObjectRequest objectRequest = new JsonObjectRequest(
                Request.Method.POST, SIGN_IN_URL, new JSONObject(params), response -> {
                    try{
                        User user = new User();
                        user.setId(response.getInt(User.KEY_ID));
                        user.setLogin(response.getString(User.KEY_LOGIN));
                        user.setPassword(response.getString(User.KEY_PASSWORD));

                        Intent intent = new Intent(getApplicationContext(),MainActivity.class);
                        intent.putExtra("login",user.getLogin());
                        intent.putExtra("id",user.getId());
                        startActivity(intent);
                        }
                    catch (JSONException e){
                        Toast.makeText(getApplicationContext(),R.string.incorrect_login,Toast.LENGTH_LONG).show();
                    }
                },
                error -> Toast.makeText(getApplicationContext(),R.string.incorrect_login,Toast.LENGTH_LONG).show());

        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(objectRequest);

    }

}

