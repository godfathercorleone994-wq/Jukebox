package com.jukebox.app;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.widget.Toast;

public class MainActivity extends Activity {
    private WebView webView;
    private static final String DEFAULT_URL = "http://localhost:5000";
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        webView = findViewById(R.id.webview);
        configureWebView();
        
        // Verifica conectividade
        if (isNetworkAvailable()) {
            loadJukeboxUrl();
        } else {
            showErrorMessage();
        }
    }
    
    private void configureWebView() {
        WebSettings webSettings = webView.getSettings();
        
        // Habilita JavaScript
        webSettings.setJavaScriptEnabled(true);
        
        // Habilita zoom
        webSettings.setSupportZoom(true);
        webSettings.setBuiltInZoomControls(true);
        webSettings.setDisplayZoomControls(false);
        
        // Configurações de armazenamento
        webSettings.setDomStorageEnabled(true);
        webSettings.setDatabaseEnabled(true);
        
        // Configurações de cache
        webSettings.setCacheMode(WebSettings.LOAD_DEFAULT);
        webSettings.setAppCacheEnabled(true);
        
        // Configurações de mídia
        webSettings.setMediaPlaybackRequiresUserGesture(false);
        
        // Configurações adicionais
        webSettings.setLoadWithOverviewMode(true);
        webSettings.setUseWideViewPort(true);
        
        // WebViewClient para manter navegação dentro do app
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onReceivedError(android.webkit.WebView view, int errorCode, 
                                       String description, String failingUrl) {
                Toast.makeText(MainActivity.this, 
                    "Erro ao carregar página: " + description, 
                    Toast.LENGTH_LONG).show();
            }
        });
        
        // WebChromeClient para suporte completo
        webView.setWebChromeClient(new WebChromeClient());
    }
    
    private void loadJukeboxUrl() {
        // URL configurável - pode ser alterada para apontar para servidor remoto
        String jukeboxUrl = getJukeboxUrl();
        webView.loadUrl(jukeboxUrl);
    }
    
    private String getJukeboxUrl() {
        // Tenta carregar URL de preferências compartilhadas
        Context context = getApplicationContext();
        android.content.SharedPreferences prefs = 
            context.getSharedPreferences("JukeboxPrefs", Context.MODE_PRIVATE);
        
        // URL padrão: localhost:5000 (para servidor local no dispositivo)
        // Para uso em produção, altere para o IP do servidor ou domínio
        String url = prefs.getString("server_url", DEFAULT_URL);
        
        // Exemplos de URLs que podem ser configuradas:
        // - http://localhost:5000 (servidor local no dispositivo)
        // - http://192.168.1.100:5000 (servidor na rede local)
        // - https://seu-dominio.com (servidor remoto)
        
        return url;
    }
    
    private void showErrorMessage() {
        Toast.makeText(this, 
            "Sem conexão com a rede. Verifique sua conexão e tente novamente.", 
            Toast.LENGTH_LONG).show();
    }
    
    private boolean isNetworkAvailable() {
        ConnectivityManager connectivityManager = 
            (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo activeNetworkInfo = connectivityManager.getActiveNetworkInfo();
        return activeNetworkInfo != null && activeNetworkInfo.isConnected();
    }
    
    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
