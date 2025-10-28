"""
Modelos do banco de dados SQLite
Define estrutura de tabelas e operações
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from contextlib import contextmanager
from src.server.config import DatabaseConfig, PaymentMethod
from src.payments import PaymentStatus


class Database:
    """Gerenciador do banco de dados SQLite"""
    
    def __init__(self, db_path: Path = None):
        self.db_path = db_path or DatabaseConfig.DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize_db()
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexões com o banco"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _initialize_db(self):
        """Cria tabelas se não existirem"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabela de transações
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id TEXT UNIQUE NOT NULL,
                    payment_method TEXT NOT NULL,
                    amount REAL NOT NULL,
                    fee REAL DEFAULT 0.0,
                    total REAL NOT NULL,
                    status TEXT NOT NULL,
                    payment_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Tabela de saldo de créditos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS credit_balance (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    balance REAL DEFAULT 0.0,
                    total_deposited REAL DEFAULT 0.0,
                    total_spent REAL DEFAULT 0.0,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Inicializa saldo se não existe
            cursor.execute("""
                INSERT OR IGNORE INTO credit_balance (id, balance) 
                VALUES (1, 0.0)
            """)
            
            # Tabela de fila de músicas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS music_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    artist TEXT,
                    duration INTEGER,
                    status TEXT DEFAULT 'queued',
                    transaction_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    played_at TIMESTAMP,
                    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
                )
            """)
            
            # Índices para performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_transactions_status 
                ON transactions(status)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_music_queue_status 
                ON music_queue(status)
            """)


class Transaction:
    """Operações relacionadas a transações de pagamento"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def create(
        self, 
        transaction_id: str,
        payment_method: PaymentMethod,
        amount: float,
        fee: float = 0.0,
        status: PaymentStatus = PaymentStatus.PENDING,
        payment_data: Optional[str] = None
    ) -> int:
        """Cria nova transação"""
        total = amount + fee
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transactions 
                (transaction_id, payment_method, amount, fee, total, status, payment_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                transaction_id,
                payment_method.value,
                amount,
                fee,
                total,
                status.value,
                payment_data
            ))
            return cursor.lastrowid
    
    def update_status(self, transaction_id: str, status: PaymentStatus) -> bool:
        """Atualiza status de uma transação"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE transactions 
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE transaction_id = ?
            """, (status.value, transaction_id))
            return cursor.rowcount > 0
    
    def get_by_id(self, transaction_id: str) -> Optional[Dict]:
        """Busca transação por ID"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM transactions WHERE transaction_id = ?
            """, (transaction_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_recent(self, limit: int = 50) -> List[Dict]:
        """Lista transações recentes"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM transactions 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_total_by_method(self, payment_method: PaymentMethod) -> float:
        """Soma total de transações aprovadas por método"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COALESCE(SUM(total), 0.0) as total
                FROM transactions
                WHERE payment_method = ? AND status = 'approved'
            """, (payment_method.value,))
            return cursor.fetchone()['total']


class CreditBalance:
    """Operações de saldo de créditos"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def get_balance(self) -> float:
        """Retorna saldo atual"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM credit_balance WHERE id = 1")
            return cursor.fetchone()['balance']
    
    def add_credit(self, amount: float) -> float:
        """Adiciona crédito ao saldo"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE credit_balance 
                SET balance = balance + ?,
                    total_deposited = total_deposited + ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
            """, (amount, amount))
            
            cursor.execute("SELECT balance FROM credit_balance WHERE id = 1")
            return cursor.fetchone()['balance']
    
    def deduct_credit(self, amount: float) -> bool:
        """Remove crédito do saldo (retorna False se saldo insuficiente)"""
        current_balance = self.get_balance()
        
        if current_balance < amount:
            return False
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE credit_balance 
                SET balance = balance - ?,
                    total_spent = total_spent + ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = 1
            """, (amount, amount))
            return True
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do saldo"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM credit_balance WHERE id = 1")
            return dict(cursor.fetchone())


class MusicQueue:
    """Operações da fila de músicas"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def add_song(
        self,
        video_id: str,
        title: str,
        artist: Optional[str] = None,
        duration: Optional[int] = None,
        transaction_id: Optional[str] = None
    ) -> int:
        """Adiciona música à fila"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO music_queue 
                (video_id, title, artist, duration, transaction_id)
                VALUES (?, ?, ?, ?, ?)
            """, (video_id, title, artist, duration, transaction_id))
            return cursor.lastrowid
    
    def get_next_song(self) -> Optional[Dict]:
        """Retorna próxima música na fila"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM music_queue 
                WHERE status = 'queued'
                ORDER BY created_at ASC
                LIMIT 1
            """)
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def mark_as_playing(self, song_id: int) -> bool:
        """Marca música como tocando"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE music_queue 
                SET status = 'playing', played_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (song_id,))
            return cursor.rowcount > 0
    
    def mark_as_played(self, song_id: int) -> bool:
        """Marca música como tocada"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE music_queue 
                SET status = 'played'
                WHERE id = ?
            """, (song_id,))
            return cursor.rowcount > 0
    
    def get_queue(self, limit: int = 10) -> List[Dict]:
        """Lista músicas na fila"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM music_queue 
                WHERE status IN ('queued', 'playing')
                ORDER BY created_at ASC
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
    
    def get_queue_size(self) -> int:
        """Retorna tamanho da fila"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) as count FROM music_queue 
                WHERE status = 'queued'
            """)
            return cursor.fetchone()['count']
    
    def clear_queue(self) -> int:
        """Limpa fila (retorna quantidade removida)"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM music_queue 
                WHERE status = 'queued'
            """)
            return cursor.rowcount
