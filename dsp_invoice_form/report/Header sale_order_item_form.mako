<html>
<head>

<script>  
   
</script>


<style>
	tr.border_header td {
  		border-top:1pt solid black;
  		border-bottom:1pt solid black;
		}
</style>
<head>
<body>
	

% for sale in objects:
<table width=100% border="0" cellscpacing="0" style="font-family:arial;font-size:12px";>
	<tr>
		<td>Sales</td>
		<td>:</td>
		<td>${sale.user_id.name}</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>Doc. Date</td>
		<td>:</td>
		<td>${sale.date_order}</td>
	</tr>
	<tr>
		<td>Term</td>
		<td>:</td>
		<td>${sale.payment_term.name}</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>Invoice Number</td>
		<td>:</td>
		<td>${sale.name}</td>
	</tr>
	<tr>
		<td>Warehouse</td>
		<td>:</td>
		
		<td>${sale.order_line[0].move_ids[0].location_id.name}</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>DO</td>
		<td>:</td>
		<td>${sale.order_line[0].move_ids[0].picking_id.name}</td>
	</tr>
	<tr>
		<td>Status</td>
		<td>:</td>
		
		% if sale.shipped == True:
			<td>Delivered</td>
		% else:
			<td>In Progress</td>
		% endif
		
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>PO</td>
		<td>:</td>
		<td>${sale.origin}</td>
	</tr>
	<tr>
		<td>Currency</td>
		<td>:</td>
		<td>${sale.pricelist_id.currency_id.name}</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>&nbsp;</td>
		<td>Customer</td>
		<td>:</td>
		<td>${sale.partner_id.name}</td>
	</tr>
</table>
</br>
</br>

<table width=100% cellscpacing="0" style="border-collapse:collapse;font-family:arial;font-size:12px";>
	<tr class="border_header">
		<td>No.</td>
		<td>Item Code</td>
		<td>Description</td>
		<td>Qty Unit</td>
		<td>Price</td>
		<td>Discount</td>
		<td>Total</td>
	</tr>
	<% n=1 %>
	% for l in sale.order_line:
		<tr>
			<td>${n}</td>
			<td>${l.product_id.default_code}</td>
			<td>${l.product_id.name}</td>
			<td>${l.product_uom_qty}</td>
			<td>${l.price_unit}</td>
			<td>${l.discount}</td>
			<td>${l.price_subtotal}</td>
		</tr>
		% for l_item in l.order_line_item:
			<tr>
				<td>&nbsp;</td>
				<td>${l_item.sub_product_id.default_code}</td>
				<td>${l_item.sub_product_id.name}</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
				<td>&nbsp;</td>
			</tr>
		% endfor
	<% n+=1 %>
	% endfor
	
</table>
% endfor
</body>
</html>