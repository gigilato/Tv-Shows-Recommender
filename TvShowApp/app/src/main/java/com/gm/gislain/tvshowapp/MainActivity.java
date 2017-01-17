package com.gm.gislain.tvshowapp;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;
import android.view.View.OnClickListener;

import com.android.volley.DefaultRetryPolicy;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.Volley;
import com.bumptech.glide.Glide;
import com.gm.gislain.tvshowapp.Model.Genre;
import com.gm.gislain.tvshowapp.Model.Show;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    private int userId;

    private final String[] SHOWS_URL = {
            "http://10.0.2.2:5000/home/shows/user/",
            "http://10.0.2.2:5000/home/shows/content/",
            "http://10.0.2.2:5000/home/shows/users/",
            "http://10.0.2.2:5000/home/shows/genre/",
            "http://10.0.2.2:5000/home/shows/genre/",
            "http://10.0.2.2:5000/home/shows/genre/",
            "http://10.0.2.2:5000/home/shows/genre/",
            "http://10.0.2.2:5000/home/shows/genre/",
            "http://10.0.2.2:5000/home/shows/genre/",
            "http://10.0.2.2:5000/home/shows/genre/",
            "http://10.0.2.2:5000/home/shows/genre/",
            "http://10.0.2.2:5000/home/shows/genre/"
    };

    private final int[] IDS = {
            R.id.layout_you_like,
            R.id.suggestion_content,
            R.id.suggestion_users,
            R.id.layout_genre1,
            R.id.layout_genre2,
            R.id.layout_genre3,
            R.id.layout_genre4,
            R.id.layout_genre5,
            R.id.layout_genre6,
            R.id.layout_genre7,
            R.id.layout_genre8,
            R.id.layout_genre9
    };

    private final int[] textviews = {
            R.id.textview_genre1,
            R.id.textview_genre2,
            R.id.textview_genre3,
            R.id.textview_genre4,
            R.id.textview_genre5,
            R.id.textview_genre6,
            R.id.textview_genre7,
            R.id.textview_genre8,
            R.id.textview_genre9
    };

    private int MARGIN_END = 20;
    private int SIZE = 500;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        userId = getIntent().getIntExtra("id",0);
        SHOWS_URL[0] += userId;
        SHOWS_URL[1] += userId;
        SHOWS_URL[2] += userId;
        getData(userId);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        //getActionBar().setDisplayShowTitleEnabled(false);

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.setDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);

        View hView =  navigationView.getHeaderView(0);
        TextView nav_user = (TextView)hView.findViewById(R.id.header_text_view);
        nav_user.setText(getIntent().getStringExtra("login"));
    }

    public void getData(final int id){
        String GENRES_URL = "http://10.0.2.2:5000/home/genre/" + id;
        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(
                GENRES_URL , new Response.Listener<JSONArray>() {
            @Override
            public void onResponse(JSONArray response) {
                for (int i = 0; i < response.length(); i++) {
                    try {
                        JSONObject object = response.getJSONObject(i);
                        SHOWS_URL[i + 3] += id + "/" + object.getInt(Genre.KEY_ID);
                        ((TextView)findViewById(textviews[i])).setText(
                                object.getString(Genre.KEY_GENRE)
                        );

                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                }

                for(int i = 0 ; i < IDS.length ; i ++) getLayoutData(i);
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(getApplicationContext(),"Error loading database",Toast.LENGTH_LONG).show();
            }
        });

        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(jsonArrayRequest);
    }

    public void getLayoutData(final int p){
        JsonArrayRequest jsonArrayRequest = new JsonArrayRequest(
                SHOWS_URL[p], new Response.Listener<JSONArray>() {
                    @Override
                    public void onResponse(JSONArray response) {
                        ArrayList<Show> shows = new ArrayList<>();

                        for (int i = 0; i < response.length(); i++) {
                            try {
                                JSONObject object = response.getJSONObject(i);
                                Show show = new Show();
                                show.setId(object.getInt(Show.KEY_ID));
                                show.setPoster(object.getString(Show.KEY_POSTER));
                                shows.add(show);

                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }

                        LinearLayout layout = (LinearLayout) findViewById(IDS[p]);

                        for (final Show show : shows){
                            ImageView imageView = new ImageView(getApplicationContext());
                            imageView.setClickable(true);
                            imageView.setScaleType(ImageView.ScaleType.FIT_CENTER);

                            imageView.setOnClickListener(new OnClickListener() {
                                @Override
                                public void onClick(View view) {
                                    Intent intent = new Intent(getApplicationContext(),ShowActivity.class);
                                    intent.putExtra("showId",show.getId());
                                    startActivity(intent);
                                }
                            });


                            LinearLayout.LayoutParams layoutParams = new LinearLayout.LayoutParams(
                                    LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);

                            layoutParams.setMarginEnd(MARGIN_END);

                            imageView.setLayoutParams(layoutParams);

                            Glide.with(getApplicationContext())
                                    .load("http://" + show.getPoster())
                                    .override(SIZE,SIZE)
                                    .into(imageView);

                            layout.addView(imageView);
                        }
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Toast.makeText(getApplicationContext(),"Error loading database",Toast.LENGTH_LONG).show();
                        error.printStackTrace();
                    }
                });

        jsonArrayRequest.setRetryPolicy(new DefaultRetryPolicy(
                1000000,
                DefaultRetryPolicy.DEFAULT_MAX_RETRIES,
                DefaultRetryPolicy.DEFAULT_BACKOFF_MULT));
        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(jsonArrayRequest);
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        int id = item.getItemId();

        if (id == R.id.nav_profile) {

        } else if (id == R.id.nav_home) {

        } else if (id == R.id.nav_search) {

        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }
}
