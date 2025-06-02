from enum import Enum

class Userstatus(Enum):
  approved='approved'
  rejected='rejected'
  pending='pending'
  blocked='blocked'
  banned='Banned'

class Orderstatus(Enum):
    pending = 'pending'
    shipped = 'shipped'
    delivered= 'delivered'
    cancelled= 'cancelled'
    failed = 'failed'

class PaymentStatus(Enum):
    pending = 'Pending'
    completed = 'completed'
    failed = 'failed'
    refunded = 'refunded'
    cancelled = 'cancelled'

# class RoleName(Enum):
#     artist = "artist"
#     buyer = "buyer"
#     admin = "admin"
  
class CategoryName(Enum):
    drawing = "drawing"
    painting = "painting"
    photography='photography'
    sculpture = "sculpture"
    handicrafts="handicrafts"
    digital = "digital" 

class StyleType(Enum):
    abstract = "abstract"
    realism = "realism"
    impressionism = "impressionism"